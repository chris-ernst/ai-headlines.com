import os
from dotenv import load_dotenv
import replicate
from pyuploadcare import Uploadcare, File

load_dotenv()

REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
public_key = os.getenv('UPLOADCARE_PUBLIC_KEY')
secret_key = os.getenv('UPLOADCARE_PRIVATE_KEY')


model = replicate.models.get("prompthero/openjourney")
version = model.versions.get(
  "9936c2001faa2194a261c01381f90e65261879985476014a0a37a334593a05eb")

promptTuning = ", highly detailed, volumetric lighting, octane render, 4k resolution, trending on artstation, masterpiece"
                # highly detailed, digital painting, artstation, concept art, smooth, sharp focus, illustration, art by artgerm and greg rutkowski and alphonse mucha, 8k



def sdCall(promptSlug):

    prompt = "mdjrny-v4 style " + promptSlug + promptTuning 
    print(prompt)

    # https://replicate.com/prompthero/openjourney/versions/9936c2001faa2194a261c01381f90e65261879985476014a0a37a334593a05eb#input
    inputs = {
    # Input prompt
    'prompt': prompt ,
    
    # Width of output image. Maximum size is 1024x768 or 768x1024 because
    # of memory limits
    'width': 512,

    # Height of output image. Maximum size is 1024x768 or 768x1024 because
    # of memory limits
    'height': 512,

    # Number of images to output
    'num_outputs': 1,

    # Number of denoising steps
    # Range: 1 to 500
    'num_inference_steps': 50,

    # Scale for classifier-free guidance
    # Range: 1 to 20
    'guidance_scale': 7,

    # Random seed. Leave blank to randomize the seed
    # 'seed': 13,
    }

    # https://replicate.com/prompthero/openjourney/versions/9936c2001faa2194a261c01381f90e65261879985476014a0a37a334593a05eb#output-schema
    output = version.predict(**inputs)
    return(output[0])




#from pyuploadcare import Uploadcare, File

def uploadCare(imgAnswer):

    uploadcare = Uploadcare(public_key, secret_key)
    imgLink = uploadcare.upload(imgAnswer)

    return(imgLink)




