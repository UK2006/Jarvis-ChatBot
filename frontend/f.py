def MainExecution():
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""
    SetAssistantStatus("Listening...")
    Query = SpeechRecognition()
    ShowTextToScreen(f"{Username}:{Query}")
    SetAssistantStatus("Thinking...")
    Decision = FirstLayerDMM(Query)
    print('')
    print(f"Decision : {Decision}")
    print("")
    G = any([ i for i in Decision if i.startswith("general")])
    R = any([i for i in Decision if i.startswith("realtime")])
    Merged_query = " and ".join(
        ["".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
    )
    for queries in Decision:
        if "generate" in queries:
            ImageGenerationQuery = str(queries)
            ImageExecution = True
    for queries in Decision:
        if TaskExecution == False:
            if any(queries.startswith(func) for func in functions):
                run(TranslateAndExecute(list(Decision)))
                TaskExecution = True
    if ImageExecution == True:
        with open(r"frontend\Files\ImageGeneration.data",'w')as file:
            file.write(f"{ImageGenerationQuery},True")
        try:
            p1 = subprocess.Popen(['python',r'backend\ImageGeneration.py'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE,shell=False)
            subprocess.append(p1)
        except Exception as e:
            print(f"Error starting ImageGeneratin.py: {e}")
    if G and R or R:
        SetAssistantStatus("Searching...")
        Answer = ChatBotResponse(QueryModifier(Merged_query))
        ShowTextToScreen(f"{Assistantname}:{Answer}")
        TextToSpeech(Answer)
        return True
    else:
        for Queries in Decision:
            if "general" in Queries:
                SetAssistantStatus("Thinking...")
                QueryFinal = Queries.replace("general","")
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname}:{Answer}")
                SetAssistantStatus("Answering...")
                TextToSpeech(Answer)
                return True
            elif "realtime" in Queries:
                SetAssistantStatus("Searchin...")
                QueryFinal = Queries.replace("realtime","")
                Answer = ChatBotResponse(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname}:{Answer}")
                SetAssistantStatus("Answering...")
                TextToSpeech(Answer)
                return True
            elif exit in Queries:
                QueryFinal = "Okay, Bye!"
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname}:{Answer}")
                SetAssistantStatus("Answering...")
                TextToSpeech(Answer)
                SetAssistantStatus("Answering...")
                os._exit(1)