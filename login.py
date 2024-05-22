import dearpygui.dearpygui as dpg
import libs.dearpygui_animate as animate

class Login():
    def __init__(self,man):
        self.man = man
        with dpg.window(tag="login",pos=[0, 0], width=300,height=300,no_title_bar=True,no_resize=True,no_move=True):
            dpg.add_spacer(height=30)
            dpg.add_text("Quizz Master!",tag="title_login",wrap=240,indent=20)
            with dpg.group(horizontal=True):
                with dpg.group():
                    dpg.add_text("Login",tag="label1_login",indent=20,wrap=280)
                with dpg.group():
                    dpg.add_combo(self.man.topic_list,callback=self.man.setTopic,width=120,tag="topic_combo")
                        
            dpg.bind_item_font(item="title_login",font="bold_font25")
            dpg.bind_item_font(item="label1_login",font="bold_font20")
            dpg.add_spacer(height=10)
            with dpg.group():
                dpg.add_input_text(hint="username",tag="username_input",width=230,indent=20)
                dpg.bind_item_font(item="username_input",font="regular_font20")
                dpg.add_spacer(height=5)
                dpg.add_input_text(hint="password",tag="password_input",password=True,width=230,indent=20)
                dpg.bind_item_font(item="password_input",font="regular_font20")

            dpg.add_spacer(height=10)
            with dpg.group(horizontal=True):
                with dpg.group():
                    dpg.add_button(label="Sign in",tag="sign_in_button",indent=20,callback=self.sign_in,height=35,width=70)
                    dpg.bind_item_theme(item="sign_in_button",theme="sign_in_theme")
                    dpg.bind_item_font(item="sign_in_button",font="bold_font20")
                with dpg.group():
                    dpg.add_button(label="Exit",tag="exit_login_button",indent=80,callback=self.exit_login,height=35,width=70)
                    dpg.bind_item_theme(item="exit_login_button",theme="exit_btn_theme")
                    dpg.bind_item_font(item="exit_login_button",font="bold_font20")
            
        with dpg.window(no_title_bar=True,modal=True,width=240,show=False,no_move=True, tag="login_popup",no_resize=True,pos=[30,100]):
            dpg.add_spacer(height=5)
            dpg.add_text("",tag="login_message",wrap=240)
            
            dpg.add_button(label="Back",tag="close_login_popup_btn", callback=self.closePopup,indent=60,height=35,width=100)
            dpg.bind_item_theme("close_login_popup_btn","exit_btn_theme")
            dpg.bind_item_font("close_login_popup_btn","bold_font20")

            dpg.add_button(label="Continue",tag="continue_sign_in_button",indent=60,callback=self.continue_login,height=35,width=100)
            dpg.bind_item_theme(item="continue_sign_in_button",theme="sign_in_theme")
            dpg.bind_item_font(item="continue_sign_in_button",font="bold_font20")


    def sign_in(self):
        usrname = dpg.get_value("username_input")
        psw = dpg.get_value("password_input")
        topic = dpg.get_value("topic_combo")
        res = self.man.requestLogin(usrname,psw,topic)
        dpg.set_value("login_message",res["label"])
        dpg.configure_item("login_popup",show=True)
        dpg.configure_item("close_login_popup_btn",show= not res["data"])
        dpg.configure_item("continue_sign_in_button",show=res["data"])


    def exit_login(self):
        dpg.stop_dearpygui()
    
    def closePopup(self):
        dpg.configure_item("login_popup",show=False)

    def continue_login(self):
        dpg.configure_item("login_popup",show=False)
        dpg.configure_item("login",show=False)
        self.man.requestData()
        