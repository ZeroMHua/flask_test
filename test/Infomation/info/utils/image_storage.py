import qiniu

access_key = 'uzc59bVURbUbazey9vrexXKocNKBUN8NuLijk57N'
secret_key = '-9lenw28jU2REojvGkcsEPWk5Nm9V2HIVqb5Nkts'

# 指定上传文件保存到哪个存储空间
bucket_name = 'gz02-info'


def storage(data):
    """上传文件到七牛云平台"""
    # 进行上传之前的初始化
    q = qiniu.Auth(access_key, secret_key)

    token = q.upload_token(bucket_name)

    # 上传文件到七牛云
    ret, info = qiniu.put_data(token, None, data)

    if info.status_code == 200:
        # 上传成功
        return ret.get('key')
    else:
        # 上传失败
        raise Exception('上传文件到七牛云失败')


if __name__ == "__main__":
    file = input('请输入您要上传的文件路径:')

    with open(file, 'rb') as f:
        storage(f.read())
