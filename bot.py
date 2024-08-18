# Import for the Web Bot
from botcity.web import WebBot, Browser, By

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

#Webdriver Manager
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd


def get_td(bot, index_column):
    """
    Captura os produtos e preços de uma coluna específica na tabela do site LME.

    Args:
        bot (WebBot): Instância do WebBot.
        index_column (int): Índice da coluna a ser processada.

    Returns:
        products: Lista de dicionários com produtos e preços
    """
    
    count = 0
    products = []
    
    while True:
        count+=1
        
        bot.scroll_down(5)
        
        bot.find_element(f'/html/body/main/div/div[1]/div[1]/div/div/table/tbody/tr/td[{index_column}]/a[{count}]', By.XPATH).click()
        bot.wait(1000)
        
        product = extract_info(bot)
        
        products.append(product)
                  
        bot.navigate_to('https://www.lme.com/en/Trading/Contract-types/Monthly-Average-Futures')    
         
        if count >= 4:
            break
        
    return products
    
    
def extract_info(bot):
    """
    Extrai informações sobre o produto e seu preço médio da página atual.

    A função utiliza um objeto `WebBot` para localizar e extrair o nome do produto e o preço médio
    da página da LME (London Metal Exchange). Os elementos são identificados por meio de seletores
    XPath e de classe CSS.

    Args:
        bot (WebBot): Instância do WebBot usada para navegar e interagir com a página web.

    Returns:
        dict: Um dicionário contendo o nome do produto e o preço médio com as seguintes chaves:
            - "Produto" (str): O nome do produto extraído da página.
            - "Preço" (str): O preço médio do produto extraído da página.
    """
    name_product = bot.find_element('/html/body/header/div[3]/div/div[1]/div/div[1]/div[3]/h1', By.XPATH).text
    avarege_price = bot.find_element('hero-metal-data__number', By.CLASS_NAME).text
    
    avarege_price = avarege_price.replace('.', ',')
    
    return {"Produto": name_product, "Preço": avarege_price}
    


def main():
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK.from_sys_args()
    ## Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = WebBot()

    # Configure whether or not to run on headless mode
    bot.headless = False

    # Uncomment to change the default Browser to Firefox
    bot.browser = Browser.CHROME

    # Uncomment to set the WebDriver path
    bot.driver_path = ChromeDriverManager().install()

    # Opens the BotCity website.
    bot.browse("https://www.lme.com/en/")
    
    #Maximize Window
    bot.maximize_window()
    
    # Implement here your logic...
    try:
        bot.navigate_to('https://www.lme.com/en/Trading/Contract-types/Monthly-Average-Futures')
        bot.wait(1000)
        
        td1 = get_td(bot, 1)
        td2 = get_td(bot, 2)
        
        data = td1 + td2
        
        df = pd.DataFrame(data)
        
        df.to_excel('Preço Médio.xlsx', index=False)
    
    except Exception as ex:
        print(ex)
        bot.save_screenshot('error.png')
    
    finally:

        # Wait 3 seconds before closing
        bot.wait(3000)

        # Finish and clean up the Web Browser
        # You MUST invoke the stop_browser to avoid
        # leaving instances of the webdriver open
        bot.stop_browser()

        # Uncomment to mark this task as finished on BotMaestro
        # maestro.finish_task(
        #     task_id=execution.task_id,
        #     status=AutomationTaskFinishStatus.SUCCESS,
        #     message="Task Finished OK."
        # )

def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
