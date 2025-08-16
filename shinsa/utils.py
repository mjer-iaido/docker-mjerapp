import qrcode
import io
import base64
from django.conf import settings
import os

def generate_membership_qr_code(testee):
    """
    会員情報を含むQRコードを生成する
    
    Args:
        testee: Testeeモデルのインスタンス
    
    Returns:
        str: base64エンコードされたQRコード画像
    """
    # QRコードに含める会員情報
    membership_data = {
        'membership_number': testee.membership_number,
        'name': testee.testee_name,
        'name_eng': testee.testee_name_eng,
        'dojo': testee.dojo.dojo_name,
        'status': str(testee.status),
        'current_grade': get_current_grade(testee)
    }
    
    # JSON形式の文字列に変換（簡易版）
    qr_text = f"会員番号: {membership_data['membership_number']}\n"
    qr_text += f"氏名: {membership_data['name']}\n"
    qr_text += f"Name: {membership_data['name_eng']}\n"
    qr_text += f"道場: {membership_data['dojo']}\n"
    qr_text += f"状態: {membership_data['status']}\n"
    qr_text += f"段位: {membership_data['current_grade']}"
    
    # QRコードを生成
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_text)
    qr.make(fit=True)
    
    # 画像を生成
    img = qr.make_image(fill_color="black", back_color="white")
    
    # base64エンコード
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return img_str

def get_current_grade(testee):
    """
    現在の段位を取得する
    
    Args:
        testee: Testeeモデルのインスタンス
    
    Returns:
        str: 現在の段位
    """
    if testee.hanshi:
        return "範士"
    elif testee.eighth_grade:
        return "八段"
    elif testee.kyoshi:
        return "教士"
    elif testee.seventh_grade:
        return "七段"
    elif testee.renshi:
        return "練士"
    elif testee.sixth_grade:
        return "六段"
    elif testee.fifth_grade:
        return "五段"
    elif testee.fourth_grade:
        return "四段"
    elif testee.third_grade:
        return "三段"
    elif testee.second_grade:
        return "二段"
    elif testee.first_grade:
        return "初段"
    else:
        return "無段"
