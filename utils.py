import joblib
import tarfile
from sagemaker import s3


def load_model_from_s3(s3_uri:str):
    """Load model from s3 using uri to model.tar.gz file
    Download the file first and then extract model from tar.gz"""
    s3.S3Downloader.download(s3_uri, '/tmp')
    return load_model_from_tarfile('/tmp/model.tar.gz')
    
    
def load_model_from_tarfile(file_path:str):
    """Extract model (joblib load) from tar.gz file"""
    t = tarfile.open(file_path, "r")
    for filename in t.getnames():
        f = t.extractfile(filename)
        model = joblib.load(f)
    
    return model