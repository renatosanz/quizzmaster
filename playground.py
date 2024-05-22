import dearpygui.dearpygui as dpg
import libs.dearpygui_animate as animate

class PlayGround(object):
    def __init__(self,man):
        self.man = man
        self.num_questions = 0
        self.current_question = 0
        self.questions = []
        self.answers = []
        self.current_answer = None


        with dpg.window(tag="playground",pos=[0, 0], width=300,show=False,height=300,no_title_bar=True,no_resize=True,no_move=True):
            dpg.add_spacer(height=30)
            dpg.add_text("",tag="title_problem")
            dpg.add_text("",tag="text_problem",wrap=280)
            dpg.bind_item_font(item="title_problem",font="bold_font20")
            dpg.bind_item_font(item="text_problem",font="regular_font20")
            dpg.add_spacer(height=10)
            with dpg.group():
                self.options = (
                dpg.add_selectable(label="op1",tag="op1"),
                dpg.add_selectable(label="op2",tag="op2"),
                dpg.add_selectable(label="op2",tag="op3"),
                dpg.add_selectable(label="op4",tag="op4"),
                )
                for a in self.options:
                    dpg.configure_item(a,callback=self._selection,user_data=self.options)
                    dpg.bind_item_font(a,"regular_font20")
            dpg.add_spacer(height=10)
            dpg.add_button(label="Next Question",tag="next_question_btn",callback=self.setUpQuestion)
            dpg.bind_item_theme("next_question_btn","exit_btn_theme")
            dpg.bind_item_font("next_question_btn","bold_font20")

        with dpg.window(no_title_bar=True,modal=True,show=False,no_move=True, tag="modal_id",no_resize=True,pos=[100,100]):
            dpg.add_text("",tag="quiz_result")
            dpg.add_button(label="Close Quiz",tag="close_quiz_btn", callback=self.closeQuiz)
            dpg.bind_item_theme("close_quiz_btn","exit_btn_theme")
            dpg.bind_item_font("close_quiz_btn","bold_font20")



    def play(self,sender,app_data,user_data):
        dpg.configure_item("playground",show=True)
        self.num_questions = user_data["difficulty"]
        self.questions = self.man.getQuestions(self.num_questions)
        self.answers = [i-i for i in range(self.num_questions)]
        animate.add("opacity","playground",0,1,[.57, .06, .61, .86], 60)
        dpg.set_value("title_problem",user_data["title"]+" Mode : "+ str(self.num_questions) +" Questions")
        dpg.set_value("text_problem",str(self.current_question+1)+". "+self.questions[self.current_question]["problem"])
        i = 0
        while i < len(self.questions[self.current_question]["options"]):
            dpg.configure_item("op"+str(i+1),label=self.questions[self.current_question]["options"][i])
            dpg.set_value("op"+str(i+1),False)
            i += 1

    def _selection(self,sender, app_data, user_data):
        self.current_answer =  dpg.get_item_label(sender)
        self.answers[self.current_question] = self.current_answer

        print(self.answers)
        for item in user_data:
              if item != sender:
                  dpg.set_value(item, False)
    
    def setUpQuestion(self,sender, app_data, user_data):
        print(1)
        if self.current_answer != None:
            print(2)
            self.current_question+=1
            if self.current_question < self.num_questions:
                dpg.set_value("text_problem",str(self.current_question+1)+". "+self.questions[self.current_question]["problem"])
                i = 0
                while i < len(self.questions[self.current_question]["options"]):
                    dpg.configure_item("op"+str(i+1),label=self.questions[self.current_question]["options"][i])
                    dpg.set_value("op"+str(i+1),False)
                    i += 1
                self.current_answer = None
            else:
                result = 0
                for i in range(self.num_questions):
                    if self.answers[i] == self.questions[i]["solution"]:
                        result += 1
                
                result = round(result/self.num_questions * 10)

                dpg.set_value("quiz_result","You got "+str(result)+"/10")
                dpg.configure_item("modal_id",show=True)
                self.current_question=0

    def closeQuiz(self):
        dpg.configure_item("modal_id", show=False)
        dpg.configure_item("playground", show=False)
