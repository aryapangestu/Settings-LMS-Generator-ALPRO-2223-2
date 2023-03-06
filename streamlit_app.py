import streamlit as st
import datetime
from datetime import date, timedelta
import base64
from PIL import Image
from cryptography.fernet import Fernet
import pandas as pd
import streamlit_nested_layout
import numpy as np
import time
import pytz


def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)


st.set_page_config(layout="wide", page_icon="🎓",
                   page_title="Generator")
st.sidebar.title("🎓 Generator ALPRO 2223-2")
right = st
left = st.sidebar

right.write("Hasil:")


left.write("Isi datanya:")

# listJenis = ["Duduk acak", "Jurnal", "TP", "Question Bank"]
listJenis = ["Duduk acak", "Jurnal"]
jenis = left.selectbox(
    "Jenis",
    listJenis,
    index=0,
)
listKelas = ["IF-46-01", "IF-46-02", "IF-46-03", "IF-46-04", "IF-46-05", "IF-46-06", "IF-46-07", "IF-46-08", "IF-46-09", "IF-46-10", "IF-46-11", "IF-46-12", "IF-46-INT",
             "IF-46-01.1PJJ", "IF-46-02.1PJJ", "IT-46-01", "IT-46-02", "IT-46-03", "IT-46-04", "SE-46-01", "SE-46-02", "SE-46-03", "SE-46-04", "DS-46-01", "DS-46-02", "DS-46-03"]
if jenis != "Question Bank" and jenis != "Duduk acak":
    kelas = left.selectbox(
        "Kelas",
        (listKelas)
    )

    nowDate = datetime.datetime.now(pytz.timezone('Asia/Jakarta'))
    if kelas == "IF-46-09" or kelas == "SE-46-04" or kelas == "IF-46-11" or kelas == "IT-46-02" or kelas == "DS-46-03" or kelas == "IF-46-05" or kelas == "IF-46-01.1PJJ":
        while nowDate.strftime("%A") != "Monday":
            nowDate = nowDate + timedelta(days=1)
    elif kelas == "IF-46-10" or kelas == "DS-46-01" or kelas == "IT-46-04" or kelas == "IF-46-02" or kelas == "SE-46-01":
        while nowDate.strftime("%A") != "Tuesday":
            nowDate = nowDate + timedelta(days=1)
    elif kelas == "IF-46-01" or kelas == "IF-46-12" or kelas == "DS-46-02" or kelas == "IF-46-INT":
        while nowDate.strftime("%A") != "Wednesday":
            nowDate = nowDate + timedelta(days=1)
    elif kelas == "IF-46-03" or kelas == "IF-46-07" or kelas == "IT-46-03" or kelas == "IF-46-02.1PJJ":
        while nowDate.strftime("%A") != "Thursday":
            nowDate = nowDate + timedelta(days=1)
    elif kelas == "IF-46-04":
        while nowDate.strftime("%A") != "Friday":
            nowDate = nowDate + timedelta(days=1)
    elif kelas == "SE-46-03" or kelas == "SE-46-02" or kelas == "IF-46-06" or kelas == "IF-46-08" or kelas == "IT-46-01":
        batas = int(nowDate.strftime("%H"))
        while nowDate.strftime("%A") != "Saturday" or batas > 10:
            nowDate = nowDate + timedelta(days=1)
            batas = -1

    if kelas == "IF-46-09" or kelas == "SE-46-04" or kelas == "IF-46-10" or kelas == "DS-46-01" or kelas == "IF-46-03":
        timeStart = datetime.time(6, 30)
    elif kelas == "SE-46-03":
        timeStart = datetime.time(7, 30)
    elif kelas == "IF-46-11" or kelas == "IT-46-04" or kelas == "IF-46-01" or kelas == "IF-46-07" or kelas == "IT-46-03":
        timeStart = datetime.time(9, 30)
    elif kelas == "SE-46-02" or kelas == "IF-46-06":
        timeStart = datetime.time(10, 30)
    elif kelas == "IT-46-02" or kelas == "IF-46-02" or kelas == "IF-46-12":
        timeStart = datetime.time(12, 30)
    elif kelas == "IF-46-04" or kelas == "IF-46-08" or kelas == "IT-46-01":
        timeStart = datetime.time(13, 30)
    elif kelas == "DS-46-03" or kelas == "IF-46-05" or kelas == "SE-46-01" or kelas == "DS-46-02" or kelas == "IF-46-INT":
        timeStart = datetime.time(15, 30)
    elif kelas == "IF-46-02.1PJJ" or kelas == "IF-46-01.1PJJ":
        timeStart = datetime.time(18, 30)

selisihWeek = 7

if jenis == "Jurnal":
    tanggalMulai = left.date_input(
        "Tanggal Mulai Praktikum",
        nowDate)
    jam = left.time_input('Jam Mulai Praktikum', timeStart)

    week = int(tanggalMulai.strftime("%V"))

    modulTP = left.number_input(
        "Modul",
        value=int(week)-selisihWeek
    )
elif jenis == "TP":
    modulTP = left.number_input(
        "Modul",
        value=(int(date.today().strftime("%V"))-(selisihWeek+1))+2
    )
elif jenis == "Question Bank":
    modulTP = left.number_input(
        "Modul",
        value=(int(date.today().strftime("%V"))-(selisihWeek+1))+2
    )
    # asesmen
    if modulTP == 7 or modulTP == 12 or modulTP == 15:
        kelas = left.selectbox(
            "Kelas",
            (listKelas)
        )
    else:
        tipeKelas = left.selectbox(
            "Tipe Kelas",
            ("REG", "INT")
        )

elif jenis == "Duduk acak":
    df = load_data(
        "https://docs.google.com/spreadsheets/d/1Tu--zAiYLB4HA3dD0OmAgaa6Vbkjyn7a/edit#gid=1051006003")

    kelas = left.selectbox(
        "Kelas",
        (df["Kelas"].drop_duplicates())
    )
    left.write('Pilih nomor meja yang tidak bisa digunakan:')
    columns = left.columns(5)
    options = []
    for i in range(5):
        for j in range(10):
            option = columns[i].checkbox(str(10 * i + j + 1))
            options.append(option)

    left.write('Pilih NIM yang tidak akan digunakan:')
    df_kelas = df[df["Kelas"] == kelas].reset_index(drop=True)
    k = 1
    A1, B1 = left.columns(2)
    for i, todo_text in df_kelas["NIM"].iteritems():
        if k >= 1 and k <= np.ceil(len(df_kelas["NIM"])/2):
            A1.checkbox(f'{todo_text}',
                        key='optionNIM_'+str(k))
            k += 1
        elif k >= np.ceil(len(df_kelas["NIM"])/2)+1 and k <= len(df_kelas["NIM"]):
            B1.checkbox(f'{todo_text}', key='optionNIM_'+str(k))
            k += 1


def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)


svg = """
        <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	 viewBox="0 0 16 16" style="enable-background:new 0 0 16 16;" xml:space="preserve">
<style type="text/css">
	.st0{fill:#FF0000;}
</style>
<path class="st0" d="M1,1.7C0.7,1.5,0.3,1.6,0.1,1.8S0,2.5,0.2,2.7L15,14.3c0.3,0.2,0.6,0.2,0.8-0.1c0.2-0.3,0.2-0.6-0.1-0.8
	l-2.6-2.1c1-1,1.7-2.2,2-3c0.1-0.2,0.1-0.4,0-0.6c-0.4-0.9-1.2-2.2-2.3-3.3c-1.2-1.1-2.8-2-4.8-2c-1.7,0-3.1,0.7-4.2,1.5L1,1.7z
	 M4.7,4.7C5.7,4,6.7,3.6,8,3.6c1.6,0,3,0.7,4,1.7c1,0.9,1.6,2,2,2.7c-0.3,0.7-0.9,1.7-1.8,2.5l-1.3-1.1C11.1,9,11.2,8.5,11.2,8
	c0-1.8-1.4-3.2-3.2-3.2c-0.8,0-1.5,0.3-2.1,0.8C5.9,5.6,4.7,4.7,4.7,4.7z M9.9,8.7l-2-1.6C7.9,6.9,8,6.7,8,6.4C8,6.3,8,6.1,8,6
	c0,0,0,0,0,0c1.1,0,2,0.9,2,2C10,8.2,10,8.5,9.9,8.7z M10.1,12c-0.6,0.3-1.3,0.4-2.1,0.4c-1.6,0-3-0.7-4-1.7C3,9.8,2.4,8.7,2,8
	c0.2-0.5,0.5-1,1-1.6L2.1,5.6c-0.6,0.7-1,1.5-1.2,2.1c-0.1,0.2-0.1,0.4,0,0.6c0.4,0.9,1.2,2.2,2.3,3.3c1.2,1.1,2.8,2,4.8,2
	c1.2,0,2.2-0.3,3.2-0.8C11.2,12.8,10.1,12,10.1,12z M4.8,8c0,1.8,1.4,3.2,3.2,3.2c0.3,0,0.7-0.1,1-0.1L7.6,9.9
	C7,9.8,6.5,9.4,6.2,8.9L4.8,7.8C4.8,7.9,4.8,7.9,4.8,8L4.8,8z"/>
</svg>
    """

svg1 = """
        <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	 viewBox="0 0 16 16" style="enable-background:new 0 0 16 16;" xml:space="preserve">
<style type="text/css">
	.st0{fill:#FF0000;}
</style>
<path class="st0" d="M8,3.1C6.2,3.1,4.7,3.9,3.6,5C2.5,6,1.8,7.2,1.4,8c0.4,0.8,1.1,2,2.2,3c1.1,1.1,2.6,1.9,4.4,1.9
	s3.3-0.8,4.4-1.9c1.1-1,1.8-2.2,2.2-3c-0.4-0.8-1.1-2-2.2-3C11.3,3.9,9.8,3.1,8,3.1z M2.7,4C4,2.8,5.8,1.8,8,1.8s4,1,5.4,2.2
	c1.3,1.2,2.2,2.7,2.6,3.6c0.1,0.2,0.1,0.5,0,0.7c-0.4,1-1.3,2.4-2.6,3.6c-1.3,1.2-3.1,2.2-5.3,2.2s-4-1-5.4-2.2
	c-1.3-1.2-2.2-2.6-2.6-3.6C0,8.1,0,7.9,0.1,7.7C0.5,6.7,1.4,5.2,2.7,4z M8,10.2c1.2,0,2.2-1,2.2-2.2S9.2,5.8,8,5.8c0,0,0,0-0.1,0
	C8,5.9,8,6.1,8,6.2C8,7.2,7.2,8,6.2,8C6.1,8,5.9,8,5.8,7.9c0,0,0,0,0,0.1C5.8,9.2,6.8,10.2,8,10.2z M8,4.4c2,0,3.6,1.6,3.6,3.6
	S10,11.6,8,11.6S4.4,10,4.4,8S6,4.4,8,4.4z"/>
</svg>
    """
b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
b641 = base64.b64encode(svg1.encode('utf-8')).decode("utf-8")

if jenis == "Question Bank":
    if modulTP == 7 or modulTP == 12 or modulTP == 15:
        key = Fernet.generate_key()
        fernet = Fernet(key)

        right.success("Video tutorial: https://youtu.be/xgSnY5P3opU")
        warningBankQUIZ = """

            ⚙️ >> ⚙️ More >> Course administration >> Question bank >> Questions

            Select a category: Asesmen Praktikum CLO 1 >> Create a new question ... >> Essay >> Add
            """
        right.warning(warningBankQUIZ, icon="⚠️")

        calMod = str(modulTP)
        right.subheader("Set setting soal di OneDrive:")
        remainder = "Share link soal dengan People in Telkom University dan Block Download ON"
        right.warning(remainder)
        image = Image.open('settingLinkSoal.png')
        right.image(image)

        if kelas != "IF-46-INT":
            right.subheader("General")
            questionname = "Question name: Asesmen Praktikum CLO 1_" + kelas
            right.write(questionname)
            right.write("Question text: ")
            desc = '\nSILAHKAN BACA ATURAN ASESMEN YANG SUDAH TERLAMPIR DI SOAL\n\nWaktu pengerjaan adalah 100 menit + 10 menit untuk waktu pengumpulan, silahkan submit sebelum waktu yang telah ditentukan. Yang dikumpulkan adalah PDF berisi SS output beserta folder Project kalian dalam bentuk rar/zip dengan format:\n1. ALPRO_MOD%s_%s_*NIM_KODEASPRAK*.pdf (Screenshot output di terminal)\n2. ALPRO_MOD%s_%s_*NIM_KODEASPRAK*.zip/rar (Go Language)\n\nCATATAN: Untuk setiap soal nama fungsi atau prosedur WAJIB menyertakan NIM, contoh: insertFirst_1301901111.\n\n**Link Soal:**\n1. 🗒️ Asesmen Praktikum CLO 1\n2. 🗒️ Project Code::Blocks.zip\n\nSelamat mengerjakan^^' % (
                calMod, kelas, calMod, kelas)
            right.write(desc)

        else:
            right.subheader("General")
            questionname = "Question name: Practicum Assessment CLO 1_" + calMod
            right.write(questionname)
            right.write("Question text: ")
            desc = '\nPLEASE READ THE ASSESSMENT RULES ATTACHED IN THE QUESTIONS\n\nThe Journal time limit is 100 minutes + 10 minutes for submitting time, please submit before the specified time. The submitted file is PDF and contains a screenshot of the output, also with your project file, zipped into .rar/.zip with the format name:\n1. ALPRO_MOD%s_%s_*SID_PRACTICUM-ASSISTANT-CODE*.pdf (Screenshot of the output in terminal)\n2. ALPRO_MOD%s_%s_*SID_PRACTICUM-ASSISTANT-CODE*.zip/rar (Go Language)\n\nNOTE: every function and procedure MUST include SID, example: insertFirst_130121XXXX\n\n**Question Links:**\n1. 🗒️ Practicum Assessment CLO 1\n2. 🗒️ Project Code::Blocks.zip\n\nGood luck^^' % (
                calMod, kelas, calMod, kelas)
            right.write(desc)

        right.subheader("Response Options")
        right.write("Response format: No online text")
        right.write("Allow attachments: Unlimited")
        right.write("Require attachments: 2")
    else:
        key = Fernet.generate_key()
        fernet = Fernet(key)

        right.success("Video tutorial: https://youtu.be/xgSnY5P3opU")
        warningBankQUIZ = """

            ⚙️ >> ⚙️ More >> Course administration >> Question bank >> Questions

            Create a new question ... >> Essay >> Add
            """
        right.warning(warningBankQUIZ, icon="⚠️")

        if tipeKelas == "REG":
            calMod = str(modulTP)
            right.subheader("Set setting soal di OneDrive:")
            remainder = "Share link soal dengan People in Telkom University dan Block Download ON"
            right.warning(remainder)
            image = Image.open('settingLinkSoal.png')
            right.image(image)

            # if calMod == "5":
            #     namaSoal = "Question name: SLL.cpp " + calMod + " REG ALPRO 2223-2"
            #     encNamaSoal = fernet.encrypt(namaSoal.encode())
            #     right.write("code SLL.cpp: " + str(encNamaSoal) + ".cpp")
            right.subheader("General")
            questionname = "Question name: Jurnal Modul " + calMod + " REG"
            right.write(questionname)
            right.write("Question text: ")
            # if calMod == "5":
            #     desc = '\nWaktu pengerjaan jurnal adalah 100 menit + 10 menit untuk waktu pengumpulan, silahkan submit sebelum waktu yang telah ditentukan. Yang dikumpulkan adalah PDF berisi SS kode dan output beserta folder Project kalian dalam bentuk rar/zip dengan format:\n1. ALPRO_MOD%s_*KELAS_NIM_KODEASPRAK*.pdf (Screenshot kode dan output di terminal)\n2. ALPRO_MOD%s_*KELAS_NIM_KODEASPRAK*.zip/rar (Go Language)\n\nCATATAN: Untuk setiap soal nama fungsi atau prosedur WAJIB menyertakan NIM, contoh: insertFirst_1301901111.\n\n**Link Soal:**\n1. 🗒️ Jurnal Modul %s\n2. 🗒️ SLL.cpp\n\nSelamat mengerjakan^^' % (
            #         calMod, calMod, calMod)
            # else:
            desc = '\nWaktu pengerjaan jurnal adalah 100 menit + 10 menit untuk waktu pengumpulan, silahkan submit sebelum waktu yang telah ditentukan. Yang dikumpulkan adalah PDF berisi SS kode dan output beserta folder Project kalian dalam bentuk rar/zip dengan format:\n1. ALPRO_MOD%s_*KELAS_NIM_KODEASPRAK*.pdf (Screenshot kode dan output di terminal)\n2. ALPRO_MOD%s_*KELAS_NIM_KODEASPRAK*.zip/rar (Go Language)\n\nCATATAN: Untuk setiap soal nama fungsi atau prosedur WAJIB menyertakan NIM, contoh: insertFirst_1301901111.\n\n**Link Soal:**\n1. 🗒️ Jurnal Modul %s\n\nSelamat mengerjakan^^' % (
                calMod, calMod, calMod)
            right.write(desc)

        elif tipeKelas == "INT":
            calMod = str(modulTP)
            right.subheader("Set setting soal di OneDrive:")
            remainder = "Share link soal dengan People in Telkom University dan Block Download ON"
            right.warning(remainder)
            image = Image.open('settingLinkSoal.png')
            right.image(image)

            # if calMod == "5":
            #     namaSoal = "Question name: SLL.cpp " + calMod + " INT ALPRO 2223-2"
            #     encNamaSoal = fernet.encrypt(namaSoal.encode())
            #     right.write("code SLL.cpp: " + str(encNamaSoal) + ".cpp")
            right.subheader("General")
            questionname = "Question name: Module Journal " + calMod + " INT"
            right.write(questionname)
            right.write("Question text: ")
            # if calMod == "5":
            #     desc = '\nThe Journal time limit is 100 minutes + 10 minutes for submitting time, please submit before the specified time. The submitted file is PDF and contains a screenshot of the source code and output, also with your project file, zipped into .rar/.zip with the format name:\n1. ALPRO_MOD%s_*CLASS_SID_PRACTICUM-ASSISTANT-CODE*.pdf (Screenshot of code and output in terminal)\n2. ALPRO_MOD%s_*CLASS_SID_PRACTICUM-ASSISTANT-CODE*.zip/rar (Go Language)\n\nNOTE: every function and procedure MUST include SID, example: insertFirst_130121XXXX\n\n**Question Links:**\n1. 🗒️ Journal Module %s\n2. 🗒️ SLL.cpp\n\nGood luck^^' % (
            #         calMod, calMod, calMod)
            # else:
            desc = '\nThe Journal time limit is 100 minutes + 10 minutes for submitting time, please submit before the specified time. The submitted file is PDF and contains a screenshot of the source code and output, also with your project file, zipped into .rar/.zip with the format name:\n1. ALPRO_MOD%s_*CLASS_SID_PRACTICUM-ASSISTANT-CODE*.pdf (Screenshot of code and output in terminal)\n2. ALPRO_MOD%s_*CLASS_SID_PRACTICUM-ASSISTANT-CODE*.zip/rar (Go Language)\n\nNOTE: every function and procedure MUST include SID, example: insertFirst_130121XXXX\n\n**Question Links:**\n1. 🗒️ Journal Module %s\n\nGood luck^^' % (
                calMod, calMod, calMod)
            right.write(desc)

        right.subheader("Response Options")
        right.write("Response format: No online text")
        right.write("Allow attachments: Unlimited")
        right.write("Require attachments: 2")
elif jenis == "Jurnal":
    calMod = str(modulTP)
    if calMod == "7" or calMod == "12" or calMod == "15":

        if kelas == "IF-46-02.1PJJ" or kelas == "IF-46-01.1PJJ":
            right.write("PJJ nanti diinfokan lagi")
        else:
            waktuPraktikum = datetime.datetime.combine(tanggalMulai, jam)
            right, video = right.columns(2)
            right.subheader("TAHAP 1")
            right.success("Video tutorial: https://youtu.be/9CtzSOxZS-4")
            warningQUIZ = """

            +Add an activity or resource >> QUIZ

            """
            right.warning(warningQUIZ, icon="⚠️")
            if kelas == "IF-46-INT":
                right.subheader("General")
                calMod = str(modulTP)
                assignmentName = "Name: Practicum Assessment CLO 1"
                right.write(assignmentName)
                right.write("Description: ")
                desc = '\nPLEASE READ THE ASSESSMENT RULES ATTACHED IN THE QUESTIONS\n\nThe Journal time limit is 100 minutes + 10 minutes for submitting time, please submit before the specified time. The submitted file is PDF and contains a screenshot of the output, also with your project file, zipped into .rar/.zip with the format name:\n1. ALPRO_MOD%s_%s_SID_PRACTICUM-ASSISTANT-CODE.pdf (Screenshot of the output in terminal)\n2. ALPRO_MOD%s_%s_SID_PRACTICUM-ASSISTANT-CODE.zip/rar (Go Language)\n\nNOTE: every function and procedure MUST include SID, example: insertFirst_130121XXXX\n\nGood luck^^' % (
                    calMod, kelas, calMod, kelas)
                right.write(desc)
            else:
                right.subheader("General")
                calMod = str(modulTP)
                assignmentName = "Name: Asesmen Praktikum CLO 1"
                right.write(assignmentName)
                right.write("Description: ")
                desc = '\nSILAHKAN BACA ATURAN ASESMEN YANG SUDAH TERLAMPIR DI SOAL\n\nWaktu pengerjaan adalah 100 menit + 10 menit untuk waktu pengumpulan, silahkan submit sebelum waktu yang telah ditentukan. Yang dikumpulkan adalah PDF berisi SS output beserta folder Project kalian dalam bentuk rar/zip dengan format:\n1. ALPRO_MOD%s_%s_NIM_KODEASPRAK.pdf (Screenshot output di terminal)\n2. ALPRO_MOD%s_%s_NIM_KODEASPRAK.zip/rar (Go Language)\n\nCATATAN: Untuk setiap soal nama fungsi atau prosedur WAJIB menyertakan NIM, contoh: insertFirst_1301901111\n\nSelamat mengerjakan^^' % (
                    calMod, kelas, calMod, kelas)
                right.write(desc)

            right.subheader("Timing")
            AllowSubmissionsFrom = waktuPraktikum + timedelta(minutes=5)
            AllowSubmissionsFromPrint = "Open the quiz: " + \
                AllowSubmissionsFrom.strftime("%d %B %Y") + " | " + \
                AllowSubmissionsFrom.strftime("%H:%M")
            right.write(AllowSubmissionsFromPrint)

            Duedate = AllowSubmissionsFrom + timedelta(minutes=120)
            DuedatePrint = "Close the quiz: " + \
                Duedate.strftime("%d %B %Y") + " | " + \
                Duedate.strftime("%H:%M")
            right.write(DuedatePrint)
            right.write("Time limit: 2 hours")

            right.subheader("Grade")
            right.write("Attempts allowed: 1")

            right.subheader("Review options")
            right.write("Semua checkbox tidak dicentang")
            image = Image.open('reviewOptions.png')
            right.image(image)

            right.subheader("Extra restrictions on attempts")
            right.write("Allowed locations: ✅ TUNE")

            right.subheader("Restrict access")
            right.write("Student: must")
            right.write("match: all")

            right.write("of the following: ")
            Group = " Group " + kelas
            htmlGroup = r'<img width="24" src="data:image/svg+xml;base64,%s"/>%s' % (
                b64, Group)
            right.write(htmlGroup, unsafe_allow_html=True)

            DateFrom = " Date: from " + AllowSubmissionsFrom.strftime(
                "%d %B %Y") + " | " + AllowSubmissionsFrom.strftime("%H:%M")
            htmlDateFrom = r'<img width="24" src="data:image/svg+xml;base64,%s"/>%s' % (
                b64, DateFrom)
            right.write(htmlDateFrom, unsafe_allow_html=True)

            DateUntil = " Date: until " + \
                Duedate.strftime("%d %B %Y") + " | " + \
                Duedate.strftime("%H:%M")
            htmlDateUntil = r'<img width="24" src="data:image/svg+xml;base64,%s"/>%s' % (
                b64, DateUntil)
            right.write(htmlDateUntil, unsafe_allow_html=True)

            right.write("SAVE")

            video.subheader("TAHAP 2")
            video.success("Video tutorial: https://youtu.be/9CtzSOxZS-4?t=271")
            warningAddQUIZ = """

            Halaman QUIZ Jurnal >> ⚙️ >> ⚙️ Edit quiz

            """
            video.warning(warningAddQUIZ, icon="⚠️")

            video.subheader("How to add questions")
            if kelas == "IF-46-INT":
                warningSettingQUIZ = """
            1. Maximum grade = 100.00 >> Save
            2. Add >> from question bank >> Select a category: Asesmen Praktikum CLO 1 >> ✅ Practicum Assessment CLO 1_%s>> Add selected questions to the quiz
            3. Edit maximum mark >> ✏️ >> 100.00 >> Enter
            """ % (kelas)
            else:
                warningSettingQUIZ = """
                1. Maximum grade = 100.00 >> Save
                2. Add >> from question bank >> Select a category: Asesmen Praktikum CLO 1 >> ✅ Asesmen Praktikum CLO 1_%s>> Add selected questions to the quiz
                3. Edit maximum mark >> ✏️ >> 100.00 >> Enter
                """ % (kelas)
            video.write(warningSettingQUIZ)
    else:
        right, video = right.columns(2)
        video.write("Hasil:")
        waktuPraktikum = datetime.datetime.combine(tanggalMulai, jam)

        if kelas == "IF-46-02.1PJJ" or kelas == "IF-46-01.1PJJ":
            right.success("Video tutorial: https://youtu.be/L7SA_LavtVg")
            warningPJJ = """
            Jurnal untuk kelas PJJ HARUS disertai video tutorial

            +Add an activity or resource >> URL
            """
            video.warning(
                warningPJJ, icon="⚠️")

            right.subheader("General Jurnal")
            calMod = str(modulTP)
            assignmentName = "Assignment name: Jurnal Modul " + calMod
            right.write(assignmentName)
            right.write("Description: ")
            desc = '\nWaktu pengerjaan adalah 100 menit + 10 menit untuk waktu pengumpulan, silahkan submit sebelum waktu yang telah ditentukan. Yang dikumpulkan adalah PDF berisi SS output beserta folder Project kalian dalam bentuk rar/zip dengan format:\n1. ALPRO_MOD%s_%s_NIM_KODEASPRAK.pdf (Screenshot output di terminal)\n2. ALPRO_MOD%s_%s_NIM_KODEASPRAK.zip/rar (Go Language)\n\nCATATAN: Untuk setiap soal nama fungsi atau prosedur WAJIB menyertakan NIM, contoh: insertFirst_1301901111.\n\nSelamat mengerjakan.' % (
                calMod, kelas, calMod, kelas)
            right.write(desc)

            right.subheader("Timing")
            AllowSubmissionsFrom = waktuPraktikum
            AllowSubmissionsFromPrint = "Open the quiz: " + \
                AllowSubmissionsFrom.strftime("%d %B %Y") + " | " + \
                AllowSubmissionsFrom.strftime("%H:%M")
            right.write(AllowSubmissionsFromPrint)

            Duedate = AllowSubmissionsFrom + timedelta(days=6)
            Duedate = Duedate.replace(hour=23, minute=59, second=59)
            DuedatePrint = "Close the quiz: " + \
                Duedate.strftime("%d %B %Y") + " | " + \
                Duedate.strftime("%H:%M")
            right.write(DuedatePrint)

            # if int(calMod) >= 1 and int(calMod) <= 7:
            #     cutOffDate = datetime.date(2022, 11, 19)
            # elif int(calMod) >= 8 and int(calMod) <= 16:
            #     cutOffDate = datetime.date(2023, 1, 14)
            # cutOffDatePrint = "Cut-off date: " + \
            #     Duedate.strftime("%d %B %Y") + " | " + \
            #     Duedate.strftime("%H:%M")
            # right.write(cutOffDatePrint)
            right.write("Time limit: 110 minutes")

            right.subheader("Grade")
            right.write("Attempts allowed: 1")

            right.subheader("Review options")
            right.write("Semua checkbox tidak dicentang")
            image = Image.open('reviewOptions.png')
            right.image(image)

            right.subheader("Restrict access")
            right.write("Student: must")
            right.write("match: all")

            right.write("of the following: ")

            activityCompletion = " Activity completion: Tugas Pendahuluan Modul 2 - " + \
                kelas + " | must be marked as complete"
            htmlGroup = r'<img width="24" src="data:image/svg+xml;base64,%s"/>%s' % (
                b641, activityCompletion)
            right.write(htmlGroup, unsafe_allow_html=True)

            Group = " Group " + kelas
            htmlGroup = r'<img width="24" src="data:image/svg+xml;base64,%s"/>%s' % (
                b64, Group)
            right.write(htmlGroup, unsafe_allow_html=True)

            DateFrom = " Date: from " + AllowSubmissionsFrom.strftime(
                "%d %B %Y") + " | " + AllowSubmissionsFrom.strftime("%H:%M")
            htmlDateFrom = r'<img width="24" src="data:image/svg+xml;base64,%s"/>%s' % (
                b64, DateFrom)
            right.write(htmlDateFrom, unsafe_allow_html=True)

            Duedate = Duedate + timedelta(days=1)
            Duedate = Duedate.replace(
                hour=00, minute=00, second=00)
            DateUntil = " Date: until " + \
                Duedate.strftime("%d %B %Y") + " | " + \
                Duedate.strftime("%H:%M")
            htmlDateUntil = r'<img width="24" src="data:image/svg+xml;base64,%s"/>%s' % (
                b64, DateUntil)
            right.write(htmlDateUntil, unsafe_allow_html=True)

            video.subheader("General Video Tutorial")
            calMod = str(modulTP)
            assignmentName = "Assignment name: Video Pembelajaran Modul " + calMod
            video.write(assignmentName)
            video.write("External URL: ")
            extURL = 'copy link video tutorial youtube di info umum'
            video.write(extURL)
            video.write("Description: ")
            desc = 'Silahkan tonton video pembelajaran untuk modul %s' % (
                calMod)
            video.write(desc)

            video.subheader("Restrict access")
            video.write("Student: must")
            video.write("match: all")

            video.write("of the following: ")
            Group = " Group " + kelas
            htmlGroup = r'<img width="24" src="data:image/svg+xml;base64,%s"/>%s' % (
                b64, Group)
            video.write(htmlGroup, unsafe_allow_html=True)

            DateFrom = " Date: from " + AllowSubmissionsFrom.strftime(
                "%d %B %Y") + " | " + AllowSubmissionsFrom.strftime("%H:%M")
            htmlDateFrom = r'<img width="24" src="data:image/svg+xml;base64,%s"/>%s' % (
                b64, DateFrom)
            video.write(htmlDateFrom, unsafe_allow_html=True)

            DateUntil = " Date: until " + \
                Duedate.strftime("%d %B %Y") + " | " + \
                Duedate.strftime("%H:%M")
            htmlDateUntil = r'<img width="24" src="data:image/svg+xml;base64,%s"/>%s' % (
                b64, DateUntil)
            video.write(htmlDateUntil, unsafe_allow_html=True)

            video.subheader("Activity completion")
            video.write(
                "Completion tracking: Show activity as complete when conditions are met")
            video.write(
                "Require view:  ✅ Student must view this activity to complete it")

        else:
            right.subheader("TAHAP 1")
            right.success("Video tutorial: https://youtu.be/9CtzSOxZS-4")
            warningQUIZ = """

            +Add an activity or resource >> QUIZ

            """
            right.warning(warningQUIZ, icon="⚠️")
            if kelas == "IF-46-INT":
                right.subheader("General")
                calMod = str(modulTP)
                assignmentName = "Name: Module Journal " + calMod
                right.write(assignmentName)
                right.write("Description: ")
                desc = '\nThe Journal time limit is 100 minutes + 10 minutes for submitting time, please submit before the specified time. The submitted file is PDF and contains a screenshot of the source code and output, also with your project file, zipped into .rar/.zip with the format name:\n1. ALPRO_MOD%s_%s_SID_PRACTICUM-ASSISTANT-CODE.pdf (Screenshot of code and output in terminal)\n2. ALPRO_MOD%s_%s_SID_PRACTICUM-ASSISTANT-CODE.zip/rar (Go Language)\n\nNOTE: every function and procedure MUST include SID, example: insertFirst_130121XXXX\n\nGood luck^^' % (
                    calMod, kelas, calMod, kelas)
                right.write(desc)
            else:
                right.subheader("General")
                calMod = str(modulTP)
                assignmentName = "Name: Jurnal Modul " + calMod
                right.write(assignmentName)
                right.write("Description: ")
                desc = '\nWaktu pengerjaan jurnal adalah 100 menit + 10 menit untuk waktu pengumpulan, silahkan submit sebelum waktu yang telah ditentukan. Yang dikumpulkan adalah PDF berisi SS kode dan output beserta folder Project kalian dalam bentuk rar/zip dengan format:\n1. ALPRO_MOD%s_%s_NIM_KODEASPRAK.pdf (Screenshot kode dan output di terminal)\n2. ALPRO_MOD%s_%s_NIM_KODEASPRAK.zip/rar (Go Language)\n\nCATATAN: Untuk setiap soal nama fungsi atau prosedur WAJIB menyertakan NIM, contoh: insertFirst_1301901111\n\nSelamat mengerjakan^^' % (
                    calMod, kelas, calMod, kelas)
                right.write(desc)

            right.subheader("Timing")
            AllowSubmissionsFrom = waktuPraktikum + timedelta(minutes=10)
            AllowSubmissionsFromPrint = "Open the quiz: " + \
                AllowSubmissionsFrom.strftime("%d %B %Y") + " | " + \
                AllowSubmissionsFrom.strftime("%H:%M")
            right.write(AllowSubmissionsFromPrint)

            Duedate = AllowSubmissionsFrom + timedelta(minutes=110)
            DuedatePrint = "Close the quiz: " + \
                Duedate.strftime("%d %B %Y") + " | " + \
                Duedate.strftime("%H:%M")
            right.write(DuedatePrint)
            right.write("Time limit: 110 minutes")

            right.subheader("Grade")
            right.write("Attempts allowed: 1")

            right.subheader("Review options")
            right.write("Semua checkbox tidak dicentang")
            image = Image.open('reviewOptions.png')
            right.image(image)

            right.subheader("Extra restrictions on attempts")
            right.write("Allowed locations: ✅ TUNE")

            right.subheader("Restrict access")
            right.write("Student: must")
            right.write("match: all")

            right.write("of the following: ")
            Group = " Group " + kelas
            htmlGroup = r'<img width="24" src="data:image/svg+xml;base64,%s"/>%s' % (
                b64, Group)
            right.write(htmlGroup, unsafe_allow_html=True)

            DateFrom = " Date: from " + AllowSubmissionsFrom.strftime(
                "%d %B %Y") + " | " + AllowSubmissionsFrom.strftime("%H:%M")
            htmlDateFrom = r'<img width="24" src="data:image/svg+xml;base64,%s"/>%s' % (
                b64, DateFrom)
            right.write(htmlDateFrom, unsafe_allow_html=True)

            DateUntil = " Date: until " + \
                Duedate.strftime("%d %B %Y") + " | " + \
                Duedate.strftime("%H:%M")
            htmlDateUntil = r'<img width="24" src="data:image/svg+xml;base64,%s"/>%s' % (
                b64, DateUntil)
            right.write(htmlDateUntil, unsafe_allow_html=True)

            right.write("Save and display")

            video.subheader("TAHAP 2")
            video.success("Video tutorial: https://youtu.be/9CtzSOxZS-4?t=271")
            warningAddQUIZ = """

            Halaman QUIZ Jurnal >> ⚙️ >> ⚙️ Edit quiz

            """
            video.warning(warningAddQUIZ, icon="⚠️")

            video.subheader("How to add questions")
            if kelas == "IF-46-INT":
                warningSettingQUIZ = """
            1. Maximum grade = 100.00 >> Save
            2. Add >> from question bank >> ✅ Module Journal %s INT>> Add selected questions to the quiz
            3. Edit maximum mark >> ✏️ >> 100.00 >> Enter
            """ % (calMod)
            else:
                warningSettingQUIZ = """
                1. Maximum grade = 100.00 >> Save
                2. Add >> from question bank >> ✅ Jurnal Modul %s REG>> Add selected questions to the quiz
                3. Edit maximum mark >> ✏️ >> 100.00 >> Enter
                """ % (calMod)
            video.write(warningSettingQUIZ)
elif jenis == "TP":
    nowDate = datetime.datetime.now(pytz.timezone('Asia/Jakarta'))

    week = int(nowDate.strftime("%V"))

    while nowDate.strftime("%A") != "Monday" or (int(week) - selisihWeek) != int(modulTP):
        nowDate = nowDate + timedelta(days=1)
        if (nowDate.strftime("%A") == "Monday"):
            week = int(nowDate.strftime("%V"))

    waktuPengumpulanTP = datetime.datetime.combine(
        nowDate, datetime.time(6, 00))

    waktuMunculTP = waktuPengumpulanTP - timedelta(days=3)
    waktuMunculTP = datetime.datetime.combine(
        waktuMunculTP, datetime.time(16, 00))

    if kelas == "IF-45-02.1PJJ" or kelas == "IF-45-01.1PJJ":
        right.write("Tidak ada TP untuk kelas ini")
    else:
        right.success("Video tutorial: https://youtu.be/L7SA_LavtVg")

        right.subheader("General")
        if kelas == "IF-46-INT":
            assignmentName = "Assignment name: Preliminary Test Module " + \
                str(modulTP)
            right.write(assignmentName)
            right.write("Description: ")
            desc = '\nThe following is an Preliminary Test for module %s of the programming algorithm course.\n\nPlease pay attention to the rules in this PT!' % (
                modulTP)
            right.write(desc)
        else:
            if kelas == "IF-46-01.1PJJ" or kelas == "IF-46-02.1PJJ":
                assignmentName = "Assignment name: Tugas Pendahuluan Modul " + \
                    str(modulTP) + " - " + kelas
            else:
                assignmentName = "Assignment name: Tugas Pendahuluan Modul " + \
                    str(modulTP)
            right.write(assignmentName)
            right.write("Description: ")
            desc = '\nBerikut merupakan tugas pendahuluan modul %s mata kuliah algoritma pemrograman.\n\nHarap perhatikan aturan yang ada pada TP ini!' % (
                modulTP)
            right.write(desc)

        right.subheader("Availability")
        AllowSubmissionsFromPrint = "Allow submissions from: " + \
            waktuMunculTP.strftime("%d %B %Y") + " | " + \
            waktuMunculTP.strftime("%H:%M")
        right.write(AllowSubmissionsFromPrint)

        week = int(nowDate.strftime("%V"))
        batasDate = nowDate
        while (int(week)-selisihWeek) < (int(batasDate.strftime("%V")) - (selisihWeek+1)):
            nowDate = nowDate + timedelta(days=1)
            if (nowDate.strftime("%A") == "Monday"):
                week = int(nowDate.strftime("%V"))

        if kelas == "IF-46-09" or kelas == "SE-46-04" or kelas == "IF-46-11" or kelas == "IT-46-02" or kelas == "DS-46-03" or kelas == "IF-46-05" or kelas == "IF-46-01.1PJJ":
            while nowDate.strftime("%A") != "Monday":
                nowDate = nowDate + timedelta(days=1)
        elif kelas == "IF-46-10" or kelas == "DS-46-01" or kelas == "IT-46-04" or kelas == "IF-46-02" or kelas == "SE-46-01":
            while nowDate.strftime("%A") != "Tuesday":
                nowDate = nowDate + timedelta(days=1)
        elif kelas == "IF-46-01" or kelas == "IF-46-12" or kelas == "DS-46-02" or kelas == "IF-46-INT":
            while nowDate.strftime("%A") != "Wednesday":
                nowDate = nowDate + timedelta(days=1)
        elif kelas == "IF-46-03" or kelas == "IF-46-07" or kelas == "IT-46-03" or kelas == "IF-46-02.1PJJ":
            while nowDate.strftime("%A") != "Thursday":
                nowDate = nowDate + timedelta(days=1)
        elif kelas == "IF-46-04":
            while nowDate.strftime("%A") != "Friday":
                nowDate = nowDate + timedelta(days=1)
        elif kelas == "SE-46-03" or kelas == "SE-46-02" or kelas == "IF-46-06" or kelas == "IF-46-08" or kelas == "IT-46-01":
            batas = int(nowDate.strftime("%H"))
            while nowDate.strftime("%A") != "Saturday" or batas > 10:
                nowDate = nowDate + timedelta(days=1)
                batas = -1

        if kelas == "IF-46-09" or kelas == "SE-46-04" or kelas == "IF-46-10" or kelas == "DS-46-01" or kelas == "IF-46-03":
            timeStart = datetime.time(6, 30)
        elif kelas == "SE-46-03":
            timeStart = datetime.time(7, 30)
        elif kelas == "IF-46-11" or kelas == "IT-46-04" or kelas == "IF-46-01" or kelas == "IF-46-07" or kelas == "IT-46-03":
            timeStart = datetime.time(9, 30)
        elif kelas == "SE-46-02" or kelas == "IF-46-06":
            timeStart = datetime.time(10, 30)
        elif kelas == "IT-46-02" or kelas == "IF-46-02" or kelas == "IF-46-12":
            timeStart = datetime.time(12, 30)
        elif kelas == "IF-46-04" or kelas == "IF-46-08" or kelas == "IT-46-01":
            timeStart = datetime.time(13, 30)
        elif kelas == "DS-46-03" or kelas == "IF-46-05" or kelas == "SE-46-01" or kelas == "DS-46-02" or kelas == "IF-46-INT":
            timeStart = datetime.time(15, 30)
        elif kelas == "IF-46-02.1PJJ" or kelas == "IF-46-01.1PJJ":
            timeStart = datetime.time(18, 30)

        if kelas == "IF-46-01.1PJJ" or kelas == "IF-46-02.1PJJ":
            waktuPengumpulanTP = datetime.datetime.combine(nowDate, timeStart)
            waktuPengumpulanTP = waktuPengumpulanTP + timedelta(days=2)
            waktuPengumpulanTP = waktuPengumpulanTP.replace(
                hour=23, minute=59, second=59)

            DuedatePrint = "Due date: " + \
                waktuPengumpulanTP.strftime("%d %B %Y") + " | " + \
                waktuPengumpulanTP.strftime("%H:%M")
            right.write(DuedatePrint)

            CutOffDatePrint = "Cut-off date: " + \
                waktuPengumpulanTP.strftime("%d %B %Y") + " | " + \
                waktuPengumpulanTP.strftime("%H:%M")
            right.write(CutOffDatePrint)
        else:
            DuedatePrint = "Due date: " + \
                waktuPengumpulanTP.strftime("%d %B %Y") + " | " + \
                waktuPengumpulanTP.strftime("%H:%M")
            right.write(DuedatePrint)

            CutOffDatePrint = "Cut-off date: " + \
                waktuPengumpulanTP.strftime("%d %B %Y") + " | " + \
                waktuPengumpulanTP.strftime("%H:%M")
            right.write(CutOffDatePrint)

        right.subheader("Submission types")
        right.write("Submission types: File submissions")
        right.write("Maximum number of uploaded files: 1")
        right.write("Maximum submission size: Course upload limit (5MB)")
        right.write(
            "Accepted file types: Document files")

        right.subheader("Grade")
        right.write("Type: Scale")
        right.write("Scale: Achievement Level")

        right.subheader("Restrict access")
        right.write("Student: must")
        right.write("match: all")

        right.write("of the following: ")
        Group = " Group " + kelas
        htmlGroup = r'<img width="24" src="data:image/svg+xml;base64,%s"/>%s' % (
            b64, Group)
        right.write(htmlGroup, unsafe_allow_html=True)

        DateFrom = " Date: from " + waktuMunculTP.strftime(
            "%d %B %Y") + " | " + waktuMunculTP.strftime("%H:%M")
        htmlDateFrom = r'<img width="24" src="data:image/svg+xml;base64,%s"/>%s' % (
            b64, DateFrom)
        right.write(htmlDateFrom, unsafe_allow_html=True)

        if kelas == "IF-46-01.1PJJ" or kelas == "IF-46-02.1PJJ":
            DateUntilTP = datetime.datetime.combine(nowDate, timeStart)
            DateUntilTP = DateUntilTP + timedelta(days=2)
            DateUntilTP = DateUntilTP.replace(hour=23, minute=59, second=59)
        else:
            DateUntilTP = datetime.datetime.combine(nowDate, timeStart)
            DateUntilTP = DateUntilTP + timedelta(minutes=60)
        DateUntil = " Date: until " + \
            DateUntilTP.strftime(
                "%d %B %Y") + " | " + DateUntilTP.strftime("%H:%M")
        htmlDateUntil = r'<img width="24" src="data:image/svg+xml;base64,%s"/>%s' % (
            b64, DateUntil)
        right.write(htmlDateUntil, unsafe_allow_html=True)

        if kelas == "IF-46-01.1PJJ" or kelas == "IF-46-02.1PJJ":
            right.subheader("Activity completion")
            right.write(
                "Completion tracking: Show activity as complete when conditions are met")
            right.write(
                "Require view: ✅ Student must submit to this activity to complete it")

elif jenis == "Duduk acak":
    # nowDate = datetime.datetime.now(pytz.timezone('Asia/Jakarta'))
    # while nowDate.strftime("%A") != "Sunday":
    #     nowDate = nowDate + timedelta(days=1)
    # timeStart = datetime.time(18, 00)
    nowDate = datetime.datetime.now(pytz.timezone('Asia/Jakarta'))
    if kelas == "IF-46-09" or kelas == "SE-46-04" or kelas == "IF-46-11" or kelas == "IT-46-02 - LAB 0604" or kelas == "IT-46-02 - LAB 0605" or kelas == "DS-46-03" or kelas == "IF-46-05" or kelas == "IF-46-01.1PJJ":
        while nowDate.strftime("%A") != "Monday":
            nowDate = nowDate + timedelta(days=1)
    elif kelas == "IF-46-10" or kelas == "DS-46-01" or kelas == "IT-46-04 - LAB 0604" or kelas == "IT-46-04 - LAB 0605" or kelas == "IF-46-02" or kelas == "SE-46-01":
        while nowDate.strftime("%A") != "Tuesday":
            nowDate = nowDate + timedelta(days=1)
    elif kelas == "IF-46-01" or kelas == "IF-46-12" or kelas == "DS-46-02" or kelas == "IF-46-INT":
        while nowDate.strftime("%A") != "Wednesday":
            nowDate = nowDate + timedelta(days=1)
    elif kelas == "IF-46-03" or kelas == "IF-46-07" or kelas == "IT-46-03" or kelas == "IF-46-02.1PJJ":
        while nowDate.strftime("%A") != "Thursday":
            nowDate = nowDate + timedelta(days=1)
    elif kelas == "IF-46-04":
        while nowDate.strftime("%A") != "Friday":
            nowDate = nowDate + timedelta(days=1)
    elif "SE-46-03 - LAB 0605" or kelas == "SE-46-03 - LAB 0617" or kelas == "SE-46-02" or kelas == "IF-46-06" or kelas == "IF-46-08" or kelas == "IT-46-01":
        batas = int(nowDate.strftime("%H"))
        while nowDate.strftime("%A") != "Saturday" or batas > 10:
            nowDate = nowDate + timedelta(days=1)
            batas = -1

    if kelas == "IF-46-09" or kelas == "SE-46-04" or kelas == "IF-46-10" or kelas == "DS-46-01" or kelas == "IF-46-03":
        timeStart = datetime.time(6, 40)
    elif kelas == "SE-46-03 - LAB 0605" or kelas == "SE-46-03 - LAB 0617":
        timeStart = datetime.time(7, 40)
    elif kelas == "IF-46-11" or kelas == "IT-46-04 - LAB 0604" or kelas == "IT-46-04 - LAB 0605" or kelas == "IF-46-01" or kelas == "IF-46-07" or kelas == "IT-46-03":
        timeStart = datetime.time(9, 40)
    elif kelas == "SE-46-02" or kelas == "IF-46-06":
        timeStart = datetime.time(10, 40)
    elif kelas == "IT-46-02 - LAB 0604" or kelas == "IT-46-02 - LAB 0605" or kelas == "IF-46-02" or kelas == "IF-46-12":
        timeStart = datetime.time(12, 40)
    elif kelas == "IF-46-04" or kelas == "IF-46-08" or kelas == "IT-46-01":
        timeStart = datetime.time(13, 40)
    elif kelas == "DS-46-03" or kelas == "IF-46-05" or kelas == "SE-46-01" or kelas == "DS-46-02" or kelas == "IF-46-INT":
        timeStart = datetime.time(15, 40)
    elif kelas == "IF-46-02.1PJJ" or kelas == "IF-46-01.1PJJ":
        timeStart = datetime.time(18, 30)
    tz = pytz.timezone('Asia/Jakarta')
    startCount = tz.localize(datetime.datetime.combine(nowDate, timeStart))
    endCount = startCount + timedelta(minutes=110)

    ph = st.empty()

    ATable, BTable, CTable, DTable, ETable = right.columns(5)
    d = []
    for x in range(1, 51):
        if (options[x-1] == True):
            d.append(x)

    def get_selected_checkboxes():
        return [i.replace('optionNIM_', '') for i in st.session_state.keys() if i.startswith('optionNIM_') and st.session_state[i]]

    NIMhapus = []
    res = [eval(i) for i in get_selected_checkboxes()]
    for x in range(1, 51):
        if (x in res):
            NIMhapus.append(int(df_kelas["NIM"][x-1]))

    def highlight(x): return ['background: red'
                              if x.name in d
                              else '' for i in x]
    df_ATemplate = pd.DataFrame()
    df_BTemplate = pd.DataFrame()
    df_CTemplate = pd.DataFrame()
    df_DTemplate = pd.DataFrame()
    df_ETemplate = pd.DataFrame()

    df_ATemplate["NO"] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    df_ATemplate["NIM"] = ["", "", "", "", "", "", "", "", "", ""]
    df_ATemplate["ASPRAK"] = ["", "", "", "", "", "", "", "", "", ""]

    df_BTemplate["NO"] = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    df_BTemplate["NIM"] = ["", "", "", "", "", "", "", "", "", ""]
    df_BTemplate["ASPRAK"] = ["", "", "", "", "", "", "", "", "", ""]

    df_CTemplate["NO"] = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    df_CTemplate["NIM"] = ["", "", "", "", "", "", "", "", "", ""]
    df_CTemplate["ASPRAK"] = ["", "", "", "", "", "", "", "", "", ""]

    df_DTemplate["NO"] = [31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
    df_DTemplate["NIM"] = ["", "", "", "", "", "", "", "", "", ""]
    df_DTemplate["ASPRAK"] = ["", "", "", "", "", "", "", "", "", ""]

    df_ETemplate["NO"] = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    df_ETemplate["NIM"] = ["", "", "", "", "", "", "", "", "", ""]
    df_ETemplate["ASPRAK"] = ["", "", "", "", "", "", "", "", "", ""]

    if ("{}".format(kelas)) not in st.session_state:
        st.session_state["{}".format(kelas)] = df[df["Kelas"] ==
                                                  kelas].sample(frac=1, random_state=int(startCount.strftime("%j"))).reset_index(drop=True)
    df_acak = st.session_state["{}".format(kelas)]
    for i in NIMhapus:
        df_acak = df_acak.drop(
            df_acak.index[(df_acak["NIM"] == int(i))], axis=0)
    df_acak = df_acak.reset_index(drop=True)

    i = 0
    for x in range(1, 51):
        if x >= 1 and x <= 10:
            if x not in d and i < len(df_acak):
                df_ATemplate["NIM"][x-1] = df_acak["NIM"][i]
                df_ATemplate["ASPRAK"][x-1] = df_acak["ASPRAK"][i]
                i += 1
        elif x >= 11 and x <= 20:
            if x not in d and i < len(df_acak):
                df_BTemplate["NIM"][x-11] = df_acak["NIM"][i]
                df_BTemplate["ASPRAK"][x-11] = df_acak["ASPRAK"][i]
                i += 1
        elif x >= 21 and x <= 30:
            if x not in d and i < len(df_acak):
                df_CTemplate["NIM"][x-21] = df_acak["NIM"][i]
                df_CTemplate["ASPRAK"][x-21] = df_acak["ASPRAK"][i]
                i += 1
        elif x >= 31 and x <= 40:
            if x not in d and i < len(df_acak):
                df_DTemplate["NIM"][x-31] = df_acak["NIM"][i]
                df_DTemplate["ASPRAK"][x-31] = df_acak["ASPRAK"][i]
                i += 1
        elif x >= 41 and x <= 50:
            if x not in d and i < len(df_acak):
                df_ETemplate["NIM"][x-41] = df_acak["NIM"][i]
                df_ETemplate["ASPRAK"][x-41] = df_acak["ASPRAK"][i]
                i += 1

    df_ATemplate = df_ATemplate.astype(
        {"NO": int, "NIM": str, "ASPRAK": str})
    df_BTemplate = df_BTemplate.astype(
        {"NO": int, "NIM": str, "ASPRAK": str})
    df_CTemplate = df_CTemplate.astype(
        {"NO": int, "NIM": str, "ASPRAK": str})
    df_DTemplate = df_DTemplate.astype(
        {"NO": int, "NIM": str, "ASPRAK": str})
    df_ETemplate = df_ETemplate.astype(
        {"NO": int, "NIM": str, "ASPRAK": str})

    # CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """
    # Inject CSS with Markdown
    ATable.markdown(hide_table_row_index, unsafe_allow_html=True)
    BTable.markdown(hide_table_row_index, unsafe_allow_html=True)
    CTable.markdown(hide_table_row_index, unsafe_allow_html=True)
    DTable.markdown(hide_table_row_index, unsafe_allow_html=True)
    ETable.markdown(hide_table_row_index, unsafe_allow_html=True)

    df_AStyler = df_ATemplate.set_index(
        'NO', drop=False).style.apply(highlight, axis=1).hide_index()
    df_BStyler = df_BTemplate.set_index(
        'NO', drop=False).style.apply(highlight, axis=1).hide_index()
    df_CStyler = df_CTemplate.set_index(
        'NO', drop=False).style.apply(highlight, axis=1).hide_index()
    df_DStyler = df_DTemplate.set_index(
        'NO', drop=False).style.apply(highlight, axis=1).hide_index()
    df_EStyler = df_ETemplate.set_index(
        'NO', drop=False).style.apply(highlight, axis=1).hide_index()

    ATable.table(df_AStyler)

    BTable.table(df_BStyler)

    CTable.table(df_CStyler)

    DTable.table(df_DStyler)

    ETable.table(df_EStyler)

    while (((datetime.datetime.now(pytz.timezone('Asia/Jakarta')) < startCount and datetime.datetime.now(pytz.timezone('Asia/Jakarta')) < endCount) or (datetime.datetime.now(pytz.timezone('Asia/Jakarta')) > startCount and datetime.datetime.now(pytz.timezone('Asia/Jakarta')) > endCount)) and (endCount - datetime.datetime.now(pytz.timezone('Asia/Jakarta'))).days >= 0):
        # calculate hours, minutes, and seconds
        secs = (startCount -
                datetime.datetime.now(pytz.timezone('Asia/Jakarta'))).seconds
        dd, hh, mm, ss = (startCount - datetime.datetime.now(pytz.timezone('Asia/Jakarta'))
                          ).days, secs//3600, (secs//60) % 60, secs % 60
        # output the countdown with hours, minutes, and seconds
        ph.metric("Praktikum dimulai dalam:",
                  f"{dd:02d}:{hh:02d}:{mm:02d}:{ss:02d}")
        time.sleep(1)

    selisih = endCount - datetime.datetime.now(pytz.timezone('Asia/Jakarta'))
    while selisih.seconds != 0 and selisih.days >= 0:
        # calculate hours, minutes, and seconds
        selisih = endCount - \
            datetime.datetime.now(pytz.timezone('Asia/Jakarta'))
        hh, mm, ss = selisih.seconds//3600, (selisih.seconds //
                                             60) % 60, selisih.seconds % 60
        # output the countdown with hours, minutes, and seconds
        if hh == 0 and mm <= 10:
            ph.metric("Waktu pengumpulan jawaban jurnal praktikum:",
                      f"{hh:02d}:{mm:02d}:{ss:02d}")
        else:
            ph.metric("Waktu pengerjaan jurnal praktikum:",
                      f"{hh:02d}:{mm:02d}:{ss:02d}")
        time.sleep(1)
    ph.write("Waktu habis!")
