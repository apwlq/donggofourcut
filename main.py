import time

from flask import Flask, redirect, url_for, render_template
import paramiko
from dotenv import load_dotenv
import os
import glob
import hashlib
import qrcode
from PIL import Image

input_image = "C:\\Users\\*\\Pictures\\"  # 이미지가 저장된 디렉터리 경로

# config sftp client
load_dotenv()
hostname = os.getenv('SFTP_HOST')
username = os.getenv('SFTP_USERNAME')
password = os.getenv('SFTP_PASSWORD')
port = 22  # SFTP default port

app = Flask(__name__)

# 기본 페이지를 렌더링하는 라우트
@app.route('/')
def index():
    return render_template('index.html')

# 버튼을 클릭했을 때 처리하는 라우트
@app.route('/bc1')
def bc1():
    myhash = hashlib.sha1(str(time.time()).encode()).hexdigest()
    remote_path = f"/home/ubuntu/data/l3c/.{myhash}.jpg"
    image_web_path = f"https://i1.lol/l3c/.{myhash}.jpg"
    qrcode_generate(image_web_path, myhash)
    # 디렉터리에서 파일들의 리스트를 가져옵니다.
    list_of_files = glob.glob(input_image + '*.JPG')
    # 파일들을 수정된 시간을 기준으로 정렬합니다.
    sorted_files = sorted(list_of_files, key=os.path.getmtime, reverse=True)
    # 최근의 4개 파일을 가져옵니다.
    recent_files = sorted_files[:4]
    imagehap("01", myhash, recent_files[3], recent_files[2], recent_files[1], recent_files[0])
    sftp_upload_file(hostname, port, username, password, f"output_image/{myhash}.jpg", remote_path)
    print(f"https://i1.lol/l3c/.{myhash}.jpg")
    return redirect(url_for('done'))

@app.route('/bc2')
def bc2():
    myhash = hashlib.sha1(str(time.time()).encode()).hexdigest()
    remote_path = f"/home/ubuntu/data/l3c/.{myhash}.jpg"
    image_web_path = f"https://i1.lol/l3c/.{myhash}.jpg"
    qrcode_generate(image_web_path, myhash)
    # 디렉터리에서 파일들의 리스트를 가져옵니다.
    list_of_files = glob.glob(input_image + '*.JPG')
    # 파일들을 수정된 시간을 기준으로 정렬합니다.
    sorted_files = sorted(list_of_files, key=os.path.getmtime, reverse=True)
    # 최근의 4개 파일을 가져옵니다.
    recent_files = sorted_files[:4]
    imagehap("02", myhash, recent_files[3], recent_files[2], recent_files[1], recent_files[0])
    sftp_upload_file(hostname, port, username, password, f"output_image/{myhash}.jpg", remote_path)
    print(f"https://i1.lol/l3c/.{myhash}.jpg")
    return redirect(url_for('done'))

@app.route('/bc3')
def bc3():
    myhash = hashlib.sha1(str(time.time()).encode()).hexdigest()
    remote_path = f"/home/ubuntu/data/l3c/.{myhash}.jpg"
    image_web_path = f"https://i1.lol/l3c/.{myhash}.jpg"
    qrcode_generate(image_web_path, myhash)
    # 디렉터리에서 파일들의 리스트를 가져옵니다.
    list_of_files = glob.glob(input_image + '*.JPG')
    # 파일들을 수정된 시간을 기준으로 정렬합니다.
    sorted_files = sorted(list_of_files, key=os.path.getmtime, reverse=True)
    # 최근의 4개 파일을 가져옵니다.
    recent_files = sorted_files[:4]
    imagehap("03", myhash, recent_files[3], recent_files[2], recent_files[1], recent_files[0])
    sftp_upload_file(hostname, port, username, password, f"output_image/{myhash}.jpg", remote_path)
    print(f"https://i1.lol/l3c/.{myhash}.jpg")
    return redirect(url_for('done'))

# 다음 페이지를 렌더링하는 라우트
@app.route('/done')
def done():
    return render_template("done.html")

def qrcode_generate(image_web_path, myhash):
    # QR 코드 생성
    qr = qrcode.QRCode(
        version=1,  # 버전 및 설정에 따라 크기 및 데이터 양이 달라집니다
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # 오류 수정 수준 설정
        box_size=10,  # 한 픽셀당 상자 크기
        border=4,  # QR 코드 주변 여백
    )
    qr.add_data(image_web_path)
    qr.make(fit=True)

    # QR 코드 이미지 생성 및 저장
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f'./qrcode_image/{myhash}.png')  # 이미지 파일로 저장
def imagehap(template_path, hash, image_path1, image_path2, image_path3, image_path4):
    # 5개의 이미지 경로
    image_paths = [
        f'theme/{template_path}.jpg',
        f'qrcode_image/{hash}.png',
        image_path1,
        image_path2,
        image_path3,
        image_path4
    ]

    # 이미지를 불러와서 리스트에 저장
    images = [Image.open(path) for path in image_paths]

    # 0번 이미지 크기 가져오기
    base_image = images[0]
    base_width, base_height = base_image.size

    width, height = images[1].size
    new_width = int(base_width * 0.3)
    new_height = int((height / width) * new_width)
    images[1] = images[1].resize((new_width, new_height))

    # 2번부터 4번 이미지 크기를 0번 이미지의 가로의 70%로 조정
    for i in range(2, 6):
        width, height = images[i].size
        new_width = int(base_width * 0.9)
        new_height = int((height / width) * new_width)
        images[i] = images[i].resize((new_width, new_height))

    # 결과 이미지 생성
    result_image = base_image.copy()

    # 2번부터 4번 이미지를 0번 이미지 위에 배치
    x_offset = (base_width - new_width) // 2  # 가운데 정렬
    y_offset = 0  # 상단 정렬

    top_margin = 100  # 상단 마진
    result_image.paste(images[2], (x_offset, y_offset + top_margin))
    y_offset += images[2].size[1] + top_margin  # 아래 마진과 다음 이미지 사이 간격

    top_margin = 50
    for img in images[3:6]:
        result_image.paste(img, (x_offset, y_offset + top_margin))
        y_offset += img.size[1] + top_margin  # 아래 마진과 다음 이미지 사이 간격

    # 오른쪽 하단에 이미지 배치
    x_offset = base_width - images[1].size[0] - 30  # 오른쪽 정렬
    y_offset = base_height - images[1].size[1] - 50  # 아래쪽 정렬
    result_image.paste(images[1], (x_offset, y_offset))
    y_offset -= images[1].size[1]  # 위로 이동하여 이미지 중첩

    result_image.convert("CMYK")  # CMYK 모드로 변환
    # 결과 이미지 저장
    result_image.save(f'output_image/{hash}.jpg')
def sftp_upload_file(hostname, port, username, password, local_file_path, remote_path):
    try:
        transport = paramiko.Transport((hostname, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        sftp.put(local_file_path, remote_path)
        print(f"File '{local_file_path}' uploaded to '{remote_path}' on the SFTP server.")

        sftp.close()
        transport.close()
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    app.run(debug=True)