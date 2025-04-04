Priscila G. Maia
Março 2025

# -*- coding: utf-8 -*-
"""automação e-mail.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1UvGhJRONakIiE_t0WhuuRgSSp89Pg_zI
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# Monta o Google Drive para acessar os arquivos
drive.mount('/content/drive')

# ID da planilha com os e-mails
email_sheet_id = "1yIJ1Rve_qcQ6zvr1jdjX0XcfKRbe1geMzy_AYvXNm_w"
email_spreadsheet = gc.open_by_key(email_sheet_id)
email_worksheet = email_spreadsheet.sheet1  #  Os e-mails estão na primeira aba

# Lendo a planilha de e-mails
email_data = email_worksheet.get_all_values()
email_df = pd.DataFrame(email_data[1:], columns=email_data[0])  # Criando um DataFrame

# Caminho da pasta com os arquivos gerados
file_path = "/content/drive/My Drive/Municipios_Separados/"

# Configuração do Gmail
email_sender = "seuemail@gmail.com"
email_password = "senha_gerada"  # Gere uma senha de aplicativo no Google

# Conectar ao servidor SMTP do Gmail
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(email_sender, email_password)

# Iterar sobre os municípios e enviar os e-mails Use para codificar com o que desejar! 
for index, row in email_df.iterrows():
    municipio_id = row["Identificador"]
    municipio_nome = row["Município"]
    destinatario = row["E-mail"]

    # Nome do arquivo esperado
    file_name = f"{municipio_id}_{especifico_nome}.xlsx"
    file_location = os.path.join(file_path, file_name)

    # Verifica se o arquivo existe antes de enviar
    if os.path.exists(file_location):
        # Criando o e-mail
        msg = MIMEMultipart()
        msg["From"] = email_sender
        msg["To"] = destinatario
        msg["Subject"] = f" ASSUNTO DO SEU E-mail - {especifico_nome}"

        # Corpo do e-mail
        body = f"Prezados,\n\nEspero que este e-mail os encontre bem. \n\nSegue anexo o {especifico_nome}. \n\nCaso haja dúvidas ou necessidade de informações adicionais, estou à disposição. \n\nAtenciosamente,\n[Seu Nome]"
        msg.attach(MIMEText(body, "plain"))

        # Anexando o arquivo
        with open(file_location, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={file_name}")
            msg.attach(part)

        # Enviar o e-mail
        server.sendmail(email_sender, destinatario, msg.as_string())
        print(f"E-mail enviado para {especifico_nome} ({destinatario}) com sucesso!")
    else:
        print(f"Arquivo não encontrado para {especifico_nome}. E-mail não enviado.")

# Fechar conexão com o servidor
server.quit()

print("Envio de e-mails concluído!")
