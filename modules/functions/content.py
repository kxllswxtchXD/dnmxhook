def content(page):
    try:
        page.wait_for_selector('pre', timeout=20000)
        pre_content = page.query_selector('pre').inner_text().strip()

        subject = page.query_selector('td:has-text("Subject:") + td')
        subject = subject.inner_text().strip() if subject else "Sem Título"

        date = page.query_selector('td:has-text("Date:") + td')
        date = date.inner_text().strip() if date else "Data desconhecida"

        to = page.query_selector('td:has-text("To:") + td')
        to = to.inner_text().strip() if to else "Destinatário desconhecido"

        return subject, date, to, pre_content
    except Exception as e:
        print(f"Erro ao extrair o conteúdo da mensagem: {e}")
        return None, None, None, None
