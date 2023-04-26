import dearpygui.dearpygui as dpg
from algorithms import Algorithm as algo


class App():
    """
        Constructor, will create main viewport and each GUI item will be
        initialised, also each item's id is as an object attribute. 
        By OMARI Hamza. 
    """
    def __init__(self):
        # APP settings attributes
        dpg.set_global_font_scale(1.75)
        # State attributes
        self.fileLoaded = False

        # Algorithm Attributes
        self.contribution = False
        self.filePath = None
        self.fileFilter = "All Files (*.*)\0*.*\0"
        self.minSup = None      #Apriori algorithm
        self.minConfidence = None

        # GUI attributes
        self.wdw_main = None
        self.wdw_plot = None
        self.wdw_minsup_row = None
        self.table_id = None
        self.plot = None
        self.btn_file = None
        self.fileDialog = None
        self.slider_minsup = None
        self.slider_minConfidence = None
        self.btn_apriori = None
        self.btn_close = None
        self.wdw_association_rules = None
        self.warningTxt = None
        self.textArea=[]

        with dpg.window(label="Main Window", no_resize=True, no_close=True,no_open_over_existing_popup=True,
         width=300, height=355, no_collapse=True, no_move=True ) as self.wdw_main:
            dpg.add_text('Apriori et Close \nTP FD\nBy zamas24')
            with dpg.file_dialog(directory_selector=False, show=False, callback=self.callback_file_dialog, file_count=3,  width=700 ,height=450) as self.fileDialog:
                dpg.add_file_extension(".csv", color=(255, 255, 0, 255))
            self.btn_file = dpg.add_button(label="Choisir un fichier",  callback=lambda: dpg.show_item(self.fileDialog))
            
            
            self.slider_minsup = dpg.add_slider_float(label="Minsup", default_value=0.5, max_value=1)
            # dpg.add_spacing(count=10)
            self.slider_minConfidence = dpg.add_slider_float(label="Min Confidence", default_value = 0.5, max_value = 1)

            
            checkbox_id = dpg.add_checkbox(label="Contribution", callback=self.callback_checkbox)

            self.btn_apriori = dpg.add_button(label='Apriori',callback = self.callback_apriori)
            # dpg.add_same_line()
            self.btn_close = dpg.add_button(label='Close', callback = self.callback_close)
            self.warningTxt = dpg.add_text("Please give a valid \nfile", color=[255,0,0], show=False)



        with dpg.window(label="Règles d'associations , Confiance, lift",show= False, no_resize=False ,no_open_over_existing_popup=True, pos=(310,0) ,width=320, height=250 ) as self.wdw_association_rules:
                 dpg.add_button(label="AddText", callback=self.callback_addText, show=False)

        with dpg.window(label="Itemsets Fréquents", show = False, no_resize=False, pos=(640,0) ,width=320, height=250 ) as self.wdw_frequent_itemsets:
             pass
        
        with dpg.window(label="Items piechart", pos=(500,300), show=False) as self.wdw_plot:

            # create plot 1
            with dpg.plot(no_title=True, no_mouse_pos=True, width=250, height=250):

                # create legend
                dpg.add_plot_legend(label="Compte de chaque item")

                # create x axis
                dpg.add_plot_axis(dpg.mvXAxis, label="", no_gridlines=True, no_tick_marks=True, no_tick_labels=True)
                dpg.set_axis_limits(dpg.last_item(), 0, 1)

                # create y axis
                with dpg.plot_axis(dpg.mvYAxis, label="", no_gridlines=True, no_tick_marks=True, no_tick_labels=True) as self.plot:
                    dpg.set_axis_limits(dpg.last_item(), 0, 1)

        # with dpg.window(label="Variation minSup et Itemset frequents",pos=(800,400), show=False)as self.wdw_minsup_row:
        #    with dpg.table(header_row=False, row_background=True,delay_search=True) as self.table_id:
        #             pass
              
    def callback_close(self): 
        dpg.delete_item(self.wdw_association_rules, children_only=True)
        dpg.delete_item(self.wdw_frequent_itemsets, children_only=True)
        dpg.delete_item(self.wdw_frequent_itemsets, children_only=True)
        dpg.delete_item(self.plot, children_only=True)
        # dpg.delete_item(self.wdw_minsup_row, children_only=True)
        if(not self.filePath):
           dpg.configure_item(self.warningTxt, show=True)
           
        else: 
            dpg.configure_item(self.warningTxt, show=False)
            dpg.configure_item(self.wdw_association_rules, show=True)
            dpg.configure_item(self.wdw_frequent_itemsets, show=True)
            # dpg.configure_item(self.wdw_minsup_row, show=True)

            minSup = dpg.get_value(self.slider_minsup)
            minConfidence = dpg.get_value(self.slider_minConfidence)
            data = algo.load_data(self.filePath)

            print("Running Apriori Algorithm with :\n")
            print("Min support = ", minSup)
            print("Min confidence = ", minConfidence)

            association_rules, closed_itemsets= algo.Close(data, minSup)
            if len(association_rules) < 1 or association_rules == None:
                 dpg.add_text("Aucune règle d'association n'est \nextraite pour ces paramètres",wrap=0, parent=self.wdw_association_rules, color=[255,0,0] )
         
            for antecedent, consequent, confidence, lift in association_rules:
                    print(f"{set(antecedent)} => {set(consequent)}")
                    paragraph1 = f"{set(antecedent)} => {set(consequent)} \tConfiance = {confidence} \t lift={lift}"
                    dpg.add_text(paragraph1, wrap=0, parent=self.wdw_association_rules)
            
            for itemset, fermeture in closed_itemsets: 
                dpg.add_text(str(set(itemset)) +" fermeture: " + str(fermeture), wrap=0, parent=self.wdw_frequent_itemsets)

            item_counts = algo.get_item_counts(data)
            items = list(item_counts.keys())
            values = list(item_counts.values())
            print(items)
            print(values)
            dpg.add_pie_series(0.5, 0.5, 0.5, values, items, parent=self.plot)

            #remplir le tableau 
            
            # if(self.contribution):
            #     for (Minsup, FI_len) in algo.minsup_FI_list:
            #         with dpg.table_row(parent=self.table_id):
            #             dpg.add_text(f" {Minsup} {FI_len}")
            #     dpg.highlight_table_column(self.table_id, 1, [0, 255, 0, 100])

    def callback_checkbox(self, sender, data):
        self.contribution = dpg.get_value(sender)
        print(f"Checkbox value: {self.contribution}")

    def callback_apriori(self): 
        dpg.delete_item(self.wdw_association_rules, children_only=True)
        dpg.delete_item(self.wdw_frequent_itemsets, children_only=True)
        dpg.delete_item(self.plot, children_only=True)
      
        
        # dpg.delete_item(self.wdw_minsup_row, children_only=True)
        if(not self.filePath):
           dpg.configure_item(self.warningTxt, show=True)
           
        else: 
            dpg.configure_item(self.warningTxt, show=False)
            dpg.configure_item(self.wdw_association_rules, show=True)
            dpg.configure_item(self.wdw_frequent_itemsets, show=True)
            

            minSup = dpg.get_value(self.slider_minsup)
            minConfidence = dpg.get_value(self.slider_minConfidence)
            data = algo.load_data(self.filePath)

            print("Running Apriori Algorithm with :\n")
            print("Min support = ", minSup)
            print("Min confidence = ", minConfidence)

            association_rules, frequent_itemsets = algo.Apriori(data, minSup, minConfidence, contribution = self.contribution)
            if len(association_rules) < 1 or association_rules == None:
                 dpg.add_text("Aucune règle d'association n'est \nextraite pour ces paramètres",wrap=0, parent=self.wdw_association_rules, color=[255,0,0] )
         
            for antecedent, consequent, confidence, lift in association_rules:
                    print(f"{set(antecedent)} => {set(consequent)}")
                    paragraph1 = f"{set(antecedent)} => {set(consequent)} \tConfiance = {confidence} \t lift={lift}"
                    dpg.add_text(paragraph1, wrap=0, parent=self.wdw_association_rules)
            
            for fi in frequent_itemsets: 
                dpg.add_text(set(fi), wrap=0, parent=self.wdw_frequent_itemsets)

            item_counts = algo.get_item_counts(data)
            items = list(item_counts.keys())
            values = list(item_counts.values())
            print(items)
            print(values)
            dpg.add_pie_series(0.5, 0.5, 0.5, values, items, parent=self.plot)
            dpg.configure_item(self.wdw_plot, show=True)

            # if(self.contribution):
            #     for (Minsup, FI_len) in algo.minsup_FI_list:
            #         dpg.add_table_column(parent=self.wdw_minsup_row)
            #         dpg.add_table_column(parent=self.wdw_minsup_row)
            #         with dpg.table_row(parent=self.table_id):
            #             dpg.add_text(f" {Minsup} {FI_len}")
            #     dpg.highlight_table_column(self.table_id, 1, [0, 255, 0, 100])
            
                     
    def callback_file_dialog(self,sender, app_data):
        self.filePath = app_data['file_path_name']
        
        if self.filePath: 
            print("File path : ", self.filePath)
            
    # For GUI Items testing purposes
    def callback_addText(self,sender, data):          
        paragraph1 = f"Sender:{sender}, data:{data}"
        txtID = dpg.add_text(paragraph1, wrap=0, parent=self.wdw_association_rules)
        self.textArea.append(txtID)

    



# Dearpygui inits stuff: 
dpg.create_context()
App()
dpg.create_viewport(title='Apriori And close', width=1080, height=720, resizable=False)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
