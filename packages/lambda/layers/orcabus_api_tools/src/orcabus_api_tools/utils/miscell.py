from urllib.parse import urlparse

def get_bucket_key_pair_from_uri(s3_uri: str) -> (str, str):
    """
    Get the bucket and key from an s3 uri
    :param s3_uri:
    :return:
    """
    url_obj = urlparse(s3_uri)

    s3_bucket = url_obj.netloc
    s3_key = url_obj.path.lstrip('/')

    if s3_bucket is None or s3_key is None:
        raise ValueError(f"Invalid S3 URI: {s3_uri}")

    return s3_bucket, s3_key
