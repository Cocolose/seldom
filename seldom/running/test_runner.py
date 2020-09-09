# coding=utf-8
import os
import time
import unittest
from xmlrunner import XMLTestRunner
import inspect
from seldom.logging import log
from seldom.driver import browser as b
from seldom.running.HTMLTestRunner import HTMLTestRunner
from seldom.running.config import Seldom, BrowserConfig


seldom_str = """
            _      _                   
           | |    | |                  
 ___   ___ | |  __| |  ___   _ __ ___  
/ __| / _ \| | / _` | / _ \ | '_ ` _ \ 
\__ \|  __/| || (_| || (_) || | | | | |
|___/ \___||_| \__,_| \___/ |_| |_| |_| 
-----------------------------------------
                             @itest.info
"""


def main(path=None,
         browser=None,
         report=None,
         title="Seldom Test Report",
         description="Test case execution",
         debug=False,
         rerun=0,
         save_last_run=False,
         driver_path=None,
         grid_url=None,
         timeout=10,
         xmlrunner=False):
    """
    runner test case
    :param path:
    :param browser:
    :param report:
    :param title:
    :param description:
    :param debug:
    :param rerun:
    :param save_last_run:
    :param driver_path:
    :param grid_url:
    :param timeout:
    :param xmlrunner:
    :return:
    """
    Seldom.application = "web"

    if path is None:
        stack_t = inspect.stack()
        ins = inspect.getframeinfo(stack_t[1][0])
        file_dir = os.path.dirname(os.path.abspath(ins.filename))
        file_path = ins.filename
        if "\\" in file_path:
            this_file = file_path.split("\\")[-1]
        elif "/" in file_path:
            this_file = file_path.split("/")[-1]
        else:
            this_file = file_path
        suits = unittest.defaultTestLoader.discover(file_dir, this_file)
    else:
        if len(path) > 3:
            if path[-3:] == ".py":
                if "/" in path:
                    path_list = path.split("/")
                    path_dir = path.replace(path_list[-1], "")
                    suits = unittest.defaultTestLoader.discover(path_dir, pattern=path_list[-1])
                else:
                    suits = unittest.defaultTestLoader.discover(os.getcwd(), pattern=path)
            else:
                suits = unittest.defaultTestLoader.discover(path)
        else:
            suits = unittest.defaultTestLoader.discover(path)
    # set browser
    if browser is None:
        BrowserConfig.name = "chrome"
    else:
        BrowserConfig.name = browser
        BrowserConfig.grid_url = grid_url

    # Set browser drive path
    if driver_path is not None:
        ret = os.path.exists(driver_path)
        if ret is False:
            raise ValueError("Browser - driven path error，Please check if the file exists. => {}".format(driver_path))
        BrowserConfig.driver_path = driver_path

    # set timeout
    if isinstance(timeout, int):
        Seldom.timeout = timeout
    else:
        raise TypeError("Timeout {} is not integer.".format(timeout))

    # set debug
    Seldom.debug = debug

    """
    Global launch browser
    """
    Seldom.driver = b(BrowserConfig.name, BrowserConfig.driver_path, BrowserConfig.grid_url)
    Seldom.driver.maximize_window()

    if debug is False:
        for filename in os.listdir(os.getcwd()):
            if filename == "reports":
                break
        else:
            os.mkdir(os.path.join(os.getcwd(), "reports"))

        if report is None:
            now = time.strftime("%Y_%m_%d_%H_%M_%S")
            if xmlrunner is False:
                report = os.path.join(os.getcwd(), "reports", now + "_result.html")
                BrowserConfig.report_path = report
            else:
                report = os.path.join(os.getcwd(), "reports", now + ".xml")
                BrowserConfig.report_path = report
        else:
            report = os.path.join(os.getcwd(), "reports", report + ".html")
            BrowserConfig.driver_path = driver_path

        with(open(report, 'wb')) as fp:
            log.info(seldom_str)
            if xmlrunner is False:
                runner = HTMLTestRunner(stream=fp, title=title, description=description)
                runner.run(suits, rerun=rerun, save_last_run=save_last_run)
            else:
                runner = XMLTestRunner(output=fp)
                runner.run(suits)
        log.info("generated html file: file:///{}".format(report))
    else:
        runner = unittest.TextTestRunner(verbosity=2)
        log.info("A run the test in debug mode without generating HTML report!")
        log.info(seldom_str)
        runner.run(suits)

    """
    Close browser globally
    """
    Seldom.driver.quit()


def app(path=None,
        command_executor=None,
        desired_capabilities=None,
        report=None,
        title="Seldom Test Report",
        description="Test case execution",
        debug=False,
        rerun=0,
        save_last_run=False,
        timeout=10):
    """
    runner test case
    :param path:
    :param command_executor:
    :param desired_capabilities:
    :param report:
    :param title:
    :param description:
    :param debug:
    :param rerun:
    :param save_last_run:
    :param timeout:
    :return:
    """
    Seldom.application = "app"

    if path is None:
        stack_t = inspect.stack()
        ins = inspect.getframeinfo(stack_t[1][0])
        file_dir = os.path.dirname(os.path.abspath(ins.filename))
        file_path = ins.filename
        if "\\" in file_path:
            this_file = file_path.split("\\")[-1]
        elif "/" in file_path:
            this_file = file_path.split("/")[-1]
        else:
            this_file = file_path
        suits = unittest.defaultTestLoader.discover(file_dir, this_file)
    else:
        if len(path) > 3:
            if path[-3:] == ".py":
                if "/" in path:
                    path_list = path.split("/")
                    path_dir = path.replace(path_list[-1], "")
                    suits = unittest.defaultTestLoader.discover(
                        path_dir, pattern=path_list[-1])
                else:
                    suits = unittest.defaultTestLoader.discover(
                        os.getcwd(), pattern=path)
            else:
                suits = unittest.defaultTestLoader.discover(path)
        else:
            suits = unittest.defaultTestLoader.discover(path)

    if command_executor is None:
        Seldom.command_executor = "http://127.0.0.1:4723/wd/hub"
    else:
        Seldom.command_executor = command_executor

    Seldom.desired_capabilities = desired_capabilities

    # set timeout
    if isinstance(timeout, int):
        Seldom.timeout = timeout
    else:
        raise TypeError("Timeout {} is not integer.".format(timeout))

    if debug is False:
        for filename in os.listdir(os.getcwd()):
            if filename == "reports":
                break
        else:
            os.mkdir(os.path.join(os.getcwd(), "reports"))

        if report is None:
            now = time.strftime("%Y_%m_%d_%H_%M_%S")
            report = os.path.join(os.getcwd(), "reports", now + "_result.html")
            BrowserConfig.report_path = report

        with(open(report, 'wb')) as fp:
            runner = HTMLTestRunner(
                stream=fp, title=title, description=description)
            log.info(seldom_str)
            runner.run(suits, rerun=rerun, save_last_run=save_last_run)
        log.info("generated html file: file:///{}".format(report))
    else:
        runner = unittest.TextTestRunner(verbosity=2)
        log.info("A run the test in debug mode without generating HTML report!")
        log.info(seldom_str)
        runner.run(suits)


if __name__ == '__main__':
    main()
