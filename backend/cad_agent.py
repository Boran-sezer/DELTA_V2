import os
import json
import asyncio
from datetime import datetime
from google import genai
from google.genai import types
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Optional

load_dotenv()

class CadAgent:
    def __init__(self, on_thought=None, on_status=None):
        api_key = os.getenv("GEMINI_API_KEY_1") or os.getenv("GEMINI_API_KEY")
        # PAS d'API v1beta - utiliser l'API standard
        self.client = genai.Client(api_key=api_key)
        # Gemini 1.5 Pro (stable et puissant pour génération de code)
        self.model = "gemini-1.5-pro"
        self.on_thought = on_thought
        self.on_status = on_status
        
        self.system_instruction = """Tu es un générateur de code Python pour la CAO 3D avec build123d.

RÈGLES ABSOLUES:
1. Réponds UNIQUEMENT avec du code Python exécutable
2. AUCUNE explication, AUCUN commentaire en dehors du bloc de code
3. Commence TOUJOURS par: from build123d import *
4. Termine TOUJOURS par: export_stl(result_part, 'output.stl')

EXEMPLES DE CODE VALIDE:

Cube simple:
```python
from build123d import *
with BuildPart() as p:
    Box(10, 10, 10)
result_part = p.part
export_stl(result_part, 'output.stl')
```

Cylindre:
```python
from build123d import *
with BuildPart() as p:
    Cylinder(radius=5, height=10)
result_part = p.part
export_stl(result_part, 'output.stl')
```

Sphère:
```python
from build123d import *
with BuildPart() as p:
    Sphere(radius=5)
result_part = p.part
export_stl(result_part, 'output.stl')
```

IMPORTANT:
- Utilise Box(), Cylinder(), Sphere(), Cone() pour les formes de base
- Dimensions en millimètres
- Garde le code SIMPLE et MINIMAL
- PAS de méthodes complexes comme fillet() ou chamfer() sauf si demandé
- TOUJOURS assigner à result_part
- TOUJOURS exporter avec export_stl()

INTERDIT:
- Texte avant ou après le code
- Explications
- Markdown sauf les délimiteurs de bloc
- Code complexe inutile
"""

    async def generate_prototype(self, prompt: str, output_dir: Optional[str] = None):
        """
        Generates 3D geometry by asking Gemini for a script, then running it LOCALLY.
        Args:
            prompt: User's description of the model to generate.
            output_dir: Directory to save the script and STL. If None, uses temp dir.
        """
        print(f"[CadAgent DEBUG] [START] Generation started for: '{prompt}'")

        try:
            # Use provided output_dir or fall back to temp
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                work_dir = output_dir
            else:
                import tempfile
                work_dir = tempfile.gettempdir()

            # Generate timestamped filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_stl = os.path.join(work_dir, f"output_{timestamp}.stl")
            script_path = os.path.join(work_dir, "current_design.py")

            # NOUVEAU: Essayer d'abord avec les templates simples
            from cad_templates import parse_simple_shape, TEMPLATES
            shape_type, params = parse_simple_shape(prompt)
            
            if shape_type and shape_type in TEMPLATES:
                print(f"[CadAgent DEBUG] [TEMPLATE] Using template for: {shape_type}")
                params['output_path'] = output_stl
                code = TEMPLATES[shape_type].format(**params)
                
                # Sauvegarder le script
                with open(script_path, "w") as f:
                    f.write(code)
                
                print(f"[CadAgent DEBUG] [EXEC] Running template script: {script_path}")
                
                # Exécuter
                import subprocess
                import sys
                try:
                    proc = await asyncio.to_thread(
                        subprocess.run,
                        [sys.executable, script_path],
                        capture_output=True,
                        text=True
                    )
                    
                    if proc.returncode == 0 and os.path.exists(output_stl):
                        print(f"[CadAgent DEBUG] [OK] Template script executed successfully.")
                        with open(output_stl, "rb") as f:
                            stl_data = f.read()
                        
                        import base64
                        b64_stl = base64.b64encode(stl_data).decode('utf-8')
                        
                        return {
                            "format": "stl",
                            "data": b64_stl,
                            "file_path": output_stl
                        }
                    else:
                        print(f"[CadAgent DEBUG] [WARN] Template failed, falling back to Gemini")
                        print(f"[CadAgent DEBUG] Error: {proc.stderr}")
                except Exception as e:
                    print(f"[CadAgent DEBUG] [WARN] Template execution failed: {e}, falling back to Gemini")

            max_retries = 2  # Réduit de 3 à 2 pour plus de rapidité
            current_prompt = f"""Génère UNIQUEMENT du code Python exécutable avec build123d pour créer: {prompt}

RÉPONDS AVEC DU CODE SEULEMENT - AUCUN TEXTE AVANT OU APRÈS.

Utilise les formes de base: Box(), Cylinder(), Sphere(), Cone()
Dimensions en millimètres.
Structure:
```python
from build123d import *
with BuildPart() as p:
    [ta forme ici]
result_part = p.part
export_stl(result_part, 'output.stl')
```"""

            for attempt in range(max_retries):
                print(f"[CadAgent DEBUG] Attempt {attempt + 1}/{max_retries}")

                # Emit status update
                if self.on_status:
                    status_info = {
                        "status": "generating" if attempt == 0 else "retrying",
                        "attempt": attempt + 1,
                        "max_attempts": max_retries,
                        "error": None
                    }
                    self.on_status(status_info)

                # 1. Ask Gemini for the code (SANS thinking pour plus de rapidité)
                raw_content = ""
                stream = await self.client.aio.models.generate_content_stream(
                    model=self.model,
                    contents=current_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_instruction,
                        temperature=0.7  # Réduit pour plus de cohérence
                    )
                )
                async for chunk in stream:
                    if chunk.candidates and chunk.candidates[0].content and chunk.candidates[0].content.parts:
                        for part in chunk.candidates[0].content.parts:
                            if part.text:
                                raw_content += part.text

                if not raw_content:
                    print("[CadAgent DEBUG] [ERR] Empty response from model.")
                    return None

                # 2. Extract Code Block
                import re
                code_match = re.search(r'```python(.*?)```', raw_content, re.DOTALL)
                if code_match:
                    code = code_match.group(1).strip()
                else:
                    # Fallback: assume entire text is code if no blocks, or fail
                    print("[CadAgent DEBUG] [WARN] No ```python block found. Trying heuristic...")
                    if "import build123d" in raw_content:
                        code = raw_content
                    else:
                        print("[CadAgent DEBUG] [ERR] Could not extract python code.")
                        return None

                # 3. Save to Local File in cad_outputs folder
                # Use raw string to handle Windows paths correctly
                with open(script_path, "w") as f:
                    # Inject output path as a raw string
                    code_with_path = code.replace("'output.stl'", f"r'{output_stl}'")
                    code_with_path = code_with_path.replace('"output.stl"', f'r"{output_stl}"')
                    f.write(code_with_path)

                print(f"[CadAgent DEBUG] [EXEC] Running local script: {script_path}")

                # 4. Execute Locally
                import subprocess
                import sys

                # Use the current Python interpreter (unified environment with build123d + mediapipe)
                try:
                    proc = await asyncio.to_thread(
                        subprocess.run,
                        [sys.executable, script_path],
                        capture_output=True,
                        text=True
                    )
                    stdout, stderr = proc.stdout, proc.stderr
                except Exception as e:
                     print(f"[CadAgent DEBUG] [ERR] Subprocess run failed: {e}")
                     proc = type('obj', (object,), {'returncode': 1})
                     stdout = ""
                     stderr = str(e)

                if proc.returncode != 0:
                    error_msg = stderr
                    # Extract a concise error message for display
                    error_lines = error_msg.strip().split('\n')
                    short_error = error_lines[-1][:100] if error_lines else "Unknown error"
                    print(f"[CadAgent DEBUG] [ERR] Script Execution Failed:\n{error_msg}")

                    # Emit retry status with error
                    if self.on_status:
                        self.on_status({
                            "status": "retrying",
                            "attempt": attempt + 1,
                            "max_attempts": max_retries,
                            "error": short_error
                        })

                    # Preparing feedback for next attempt
                    current_prompt = f"""
    The Python script you generated failed to execute with the following error:
    {error_msg}

    Please fix the code to resolve this error. Return the full corrected script. 
    Ensure you still export to 'output.stl'.
    Original request: {prompt}
    """
                    continue # Retry loop

                print(f"[CadAgent DEBUG] [OK] Script executed successfully.")

                # 5. Read Output
                if os.path.exists(output_stl):
                    print(f"[CadAgent DEBUG] [file] '{output_stl}' found.")
                    with open(output_stl, "rb") as f:
                        stl_data = f.read()

                    import base64
                    b64_stl = base64.b64encode(stl_data).decode('utf-8')

                    return {
                        "format": "stl",
                        "data": b64_stl,
                        "file_path": output_stl
                    }
                else:
                     print(f"[CadAgent DEBUG] [ERR] '{output_stl}' was not generated.")
                     # If script ran but no output, treat as failure and retry?
                     # Ideally yes.
                     current_prompt = f"The script executed successfully but 'output.stl' was not found. Ensure you call `export_stl(result_part, 'output.stl')` at the end."
                     continue

            # If loop finishes without success
            print("[CadAgent DEBUG] [ERR] All attempts failed.")
            if self.on_status:
                self.on_status({
                    "status": "failed",
                    "attempt": max_retries,
                    "max_attempts": max_retries,
                    "error": "All generation attempts failed"
                })
            return None

        except Exception as e:
            print(f"CadAgent Error: {e}")
            import traceback
            traceback.print_exc()
            return None

    async def iterate_prototype(self, prompt: str, output_dir: Optional[str] = None):
        """
        Iterates on the existing design by reading 'current_design.py' and applying changes.
        Args:
            prompt: User's description of the changes to make.
            output_dir: Directory containing existing script and where to save new STL.
        """
        print(f"[CadAgent DEBUG] [START] Iteration started for: '{prompt}'")
        
        # Use provided output_dir or fall back to temp
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            work_dir = output_dir
        else:
            import tempfile
            work_dir = tempfile.gettempdir()
        
        # Generate timestamped filename for the output
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        script_path = os.path.join(work_dir, "current_design.py")
        output_stl = os.path.join(work_dir, f"output_{timestamp}.stl")
        
        existing_code = ""
        
        if os.path.exists(script_path):
            with open(script_path, "r") as f:
                existing_code = f.read()
            
            # Sanitize existing code: replace any absolute paths with 'output.stl'
            # This prevents the LLM from seeing/reproducing Windows paths that cause Unicode escape errors
            import re
            # Match both escaped (\\) and unescaped (\) Windows paths to output.stl
            existing_code = re.sub(
                r"['\"]C:\\\\?Users\\\\?[^'\"]+\\\\?output[^'\"]*\.stl['\"]",
                "'output.stl'",
                existing_code
            )
            # Also handle forward-slash variants
            existing_code = re.sub(
                r"['\"]C:/Users/[^'\"]+/output[^'\"]*\.stl['\"]",
                "'output.stl'",
                existing_code
            )
        else:
             print("[CadAgent DEBUG] [WARN] No existing script found. Falling back to fresh generation.")
             return await self.generate_prototype(prompt)

        try:

            max_retries = 2  # Réduit de 3 à 2 pour plus de rapidité
            current_prompt = f"""
You are iterating on an existing 3D model script.

Current Python Code:
```python
{existing_code}
```

User Request: {prompt}

Task: Rewrite the code to satisfy the user's request while maintaining the rest of the model structure.
Ensure you still export to 'output.stl'.
"""
            
            for attempt in range(max_retries):
                print(f"[CadAgent DEBUG] Iteration Attempt {attempt + 1}/{max_retries}")
                
                # Emit status update
                if self.on_status:
                    status_info = {
                        "status": "generating" if attempt == 0 else "retrying",
                        "attempt": attempt + 1,
                        "max_attempts": max_retries,
                        "error": None
                    }
                    self.on_status(status_info)
                
                # 1. Ask Gemini for the code (SANS thinking pour rapidité)
                raw_content = ""
                stream = await self.client.aio.models.generate_content_stream(
                    model=self.model,
                    contents=current_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_instruction,
                        temperature=0.7  # Réduit pour cohérence
                    )
                )
                async for chunk in stream:
                    if chunk.candidates and chunk.candidates[0].content and chunk.candidates[0].content.parts:
                        for part in chunk.candidates[0].content.parts:
                            if part.text:
                                raw_content += part.text
                
                if not raw_content:
                    print("[CadAgent DEBUG] [ERR] Empty response from model.")
                    return None

                # 2. Extract Code Block
                import re
                code_match = re.search(r'```python(.*?)```', raw_content, re.DOTALL)
                if code_match:
                    code = code_match.group(1).strip()
                else:
                    # Fallback: assume entire text is code if no blocks, or fail
                    print("[CadAgent DEBUG] [WARN] No ```python block found. Trying heuristic...")
                    if "import build123d" in raw_content:
                        code = raw_content
                    else:
                        print("[CadAgent DEBUG] [ERR] Could not extract python code.")
                        return None
                
                # 3. Save to Local File in cad_outputs folder
                # Overwrite the script so the next iteration builds on this one
                
                # Use raw string to handle Windows paths correctly
                with open(script_path, "w") as f:
                    # Inject output path as a raw string
                    code_with_path = code.replace("'output.stl'", f"r'{output_stl}'")
                    code_with_path = code_with_path.replace('"output.stl"', f'r"{output_stl}"')
                    f.write(code_with_path)
                    
                print(f"[CadAgent DEBUG] [EXEC] Running local script: {script_path}")
                
                # 4. Execute Locally
                import subprocess
                import sys
                
                # Use asyncio.to_thread for Windows compatibility (asyncio.create_subprocess_exec
                # throws NotImplementedError on Windows with certain event loop policies)
                try:
                    proc = await asyncio.to_thread(
                        subprocess.run,
                        [sys.executable, script_path],
                        capture_output=True,
                        text=True
                    )
                    stdout, stderr = proc.stdout, proc.stderr
                except Exception as e:
                    print(f"[CadAgent DEBUG] [ERR] Subprocess run failed: {e}")
                    proc = type('obj', (object,), {'returncode': 1})()
                    stdout = ""
                    stderr = str(e)
                
                if proc.returncode != 0:
                    error_msg = stderr
                    print(f"[CadAgent DEBUG] [ERR] Script Execution Failed:\n{error_msg}")
                    
                    # Preparing feedback for next attempt
                    current_prompt = f"""
The updated Python script you generated failed to execute with the following error:
{error_msg}

Please fix the code to resolve this error. Return the full corrected script. 
Ensure you still export to 'output.stl'.
"""
                    continue # Retry loop
                
                print(f"[CadAgent DEBUG] [OK] Script executed successfully.")
                
                # 5. Read Output
                if os.path.exists(output_stl):
                    print(f"[CadAgent DEBUG] [file] '{output_stl}' found.")
                    with open(output_stl, "rb") as f:
                        stl_data = f.read()
                        
                    import base64
                    b64_stl = base64.b64encode(stl_data).decode('utf-8')
                    
                    return {
                        "format": "stl",
                        "data": b64_stl,
                        "file_path": output_stl
                    }
                else:
                     print(f"[CadAgent DEBUG] [ERR] '{output_stl}' was not generated.")
                     current_prompt = f"The script executed successfully but '{output_stl}' was not found. Ensure you call `export_stl(result_part, 'output.stl')` at the end."
                     continue

            # If loop finishes without success
            print("[CadAgent DEBUG] [ERR] All attempts failed.")
            if self.on_status:
                self.on_status({
                    "status": "failed",
                    "attempt": max_retries,
                    "max_attempts": max_retries,
                    "error": "All iteration attempts failed"
                })
            return None

        except Exception as e:
            print(f"CadAgent Error: {e}")
            import traceback
            traceback.print_exc()
            return None
