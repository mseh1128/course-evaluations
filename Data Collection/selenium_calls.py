from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time

# Create a new instance of the Firefox driver

options = Options()
options.set_headless(headless=True)
driver = webdriver.Firefox(firefox_options=options)
# # go to the google home page
driver.get("https://psns.cc.stonybrook.edu/psp/csprodg/EMPLOYEE/CAMP/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL?FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HC_CLASS_SEARCH_GBL&IsFolder=false&IgnoreParamTempl=FolderPath,IsFolder")
driver.switch_to_frame("TargetContent")

subject = driver.find_element_by_css_selector('#SSR_CLSRCH_WRK_SUBJECT\$0')
subject.send_keys("lds")

course_number = driver.find_element_by_id("SSR_CLSRCH_WRK_CATALOG_NBR$1")
course_number.send_keys("102")

time.sleep(0.3)  # healthy ~0.15sxs "loading margin"
login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH")))
login.click()

i = 0
professor_names = set()
# while (True):
#     try:
#         instructor = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'win0divMTG_INSTR$' + str
#                                                                                      (i))))
#         professor_names.add(instructor.text)
#         i += 1
#     except Exception:
#         # print(e)
#         break

# for i in professor_names:
#     print(i)


num_of_sections = driver.find_element_by_class_name('PSPAGECONTAINER')
print(num_of_sections.innerHTML)


# for i in range(1, 10):
#     first_instuctor = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'win0divMTG_INSTR$' + str(i))))
#     print(first_instuctor.text)

driver.quit()
