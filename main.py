import streamlit as st
import qrcode
from PIL import Image
from pyzbar.pyzbar import decode
from io import BytesIO

st.set_page_config(page_title="QR Code Generator & Scanner", layout="centered")
st.title(" QR Code Generator & Scanner")

# Tabs 
tab1, tab2 = st.tabs([" Generate QR", " Scan QR"])

# QR Generator 
with tab1:
    st.header(" Generate QR Code")

    qr_text = st.text_input("Enter text or URL to generate QR")

    # QR colors
    fg_color = st.color_picker("Choose QR color", "#000000")  # black
    bg_color = st.color_picker("Choose background color", "#ffffff")  # white

    # Optional logo upload
    uploaded_logo = st.file_uploader("Upload a logo to embed (optional)", type=["png", "jpg", "jpeg"])

    generate_btn = st.button("Generate QR Code")

    if generate_btn and qr_text:
        # Create QR code with custom settings
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_text)
        qr.make(fit=True)

        # Generate QR image with selected colors
        qr_img = qr.make_image(fill_color=fg_color, back_color=bg_color).convert('RGB')

        # If user uploaded a logo, paste it in the center
        if uploaded_logo:
            logo = Image.open(uploaded_logo)
            logo_size = 50
            logo = logo.resize((logo_size, logo_size))
            pos = ((qr_img.size[0] - logo_size) // 2, (qr_img.size[1] - logo_size) // 2)
            qr_img.paste(logo, pos)

        # Save QR to buffer
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        buffer.seek(0)

        # Show and download
        st.image(buffer, caption="Generated QR Code", use_container_width=False)

        st.download_button(
            label="Download QR Code",
            data=buffer.getvalue(),
            file_name="custom_qr.png",
            mime="image/png"
        )



# QR Scanner 
with tab2:
    st.header("Scan QR Code from Image")

    uploaded_file = st.file_uploader("Upload an image with a QR code", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded QR Image", use_column_width=False)

        decoded_objs = decode(image)
        if decoded_objs:
            st.success("QR Code(s) Found:")
            for obj in decoded_objs:
                st.code(obj.data.decode("utf-8"), language="text")
        else:
            st.error(" No QR code found in the image.")
