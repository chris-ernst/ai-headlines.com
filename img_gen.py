import os
from dotenv import load_dotenv
import replicate
from pyuploadcare import Uploadcare, File

load_dotenv()

REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
public_key = os.getenv('UPLOADCARE_PUBLIC_KEY')
secret_key = os.getenv('UPLOADCARE_PRIVATE_KEY')


promptTuning = ", realistic photo, associated press picture"

def sdCall(promptSlug):

    prompt = promptSlug + promptTuning
    print(prompt)

    output = replicate.run(
        "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        input={
            "width": 1024,
            "height": 1024,
            'prompt': prompt,
            "refine": "expert_ensemble_refiner",
            "scheduler": "K_EULER",
            "lora_scale": 0.6,
            "num_outputs": 1,
            "guidance_scale": 7.5,
            "apply_watermark": False,
            "high_noise_frac": 0.8,
            "negative_prompt": "",
            "prompt_strength": 0.8,
            "num_inference_steps": 50
        }
    )
    print(output)
    return(output)




def uploadCare(imgAnswer):
    uploadcare = Uploadcare(public_key, secret_key)
    imgLink = uploadcare.upload_from_url_sync(
        imgAnswer,
        check_duplicates=True,
        save_duplicates=False
    )
    imgLink = f"{imgLink}-/preview/1000x1000/"
    return(imgLink)





