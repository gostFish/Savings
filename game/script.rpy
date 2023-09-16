define us = Character("Malcolm and Simon",who_font="SUBWT___.ttf")
define cr = Character("ClassRoom",who_font="SUBWT___.ttf")
define tc = Character("Teacher",who_font="SUBWT___.ttf")
define sp = Character("spouse",who_font="SUBWT___.ttf")
define pn = Character("Partner",who_font="SUBWT___.ttf")
define ll = Character("Landlord",who_font="SUBWT___.ttf")
define boss = Character("Boss",who_font="SUBWT___.ttf")
define nar = Character(" ",kind=nvl,what_bold=True, what_color="#f2ff00")
define warn = Character(" ",kind=nvl,what_bold=True, what_color="#ffff00")

define menu = nvl_menu
define gui.text_font = "SUBWT___.ttf"

define gui.nvl_spacing = 0.1
define gui.text_size = 24

define gui.nvl_name_width = 740
define gui.nvl_text_width = 740
define gui.nvl_thought_width = 740

define gui.about = "This project has been developed by Malcolm Grech and Simon Xerri for the ARI3216 Assignment project\n\nTo Play you must select the various choice options when they are presented and click anywhere on the screen to proceed in the dialogue"

init python:
    import subprocess
    import os
    import re

    fileLoc = os.path.abspath(os.path.join(config.basedir, "game\webscraper"))

    doc = open(fileLoc + "\Information.txt","w")
    subprocess.call(fileLoc + "\GetWebInfo.exe",stdout=doc)
    doc.close()

    with open(os.path.join(fileLoc,'Information.txt'), 'r') as f:
        Data = f.read()
    Data = Data.replace(",","")

    uRate = re.findall(r"UnemplyomentRate: (.*?)", Data)
    allLowBound = re.findall(r"From (.*?) to", Data)
    allHighBound = re.findall(r"to (.*?) rate", Data)
    allRate = re.findall(r"rate: (.*?) deduct", Data)

    lowBound = []
    highBound = []
    rate = []

    for x in range(4):  #For this implementation get only the first 5 intervals (Married person rates (easier for player))
        lowBound.append(allLowBound[x])
        highBound.append(allHighBound[x])
        rate.append(allRate[x])


init python:

    style.nvl_menu_choice.idle_color = "#000000DD"
    style.nvl_menu_choice.hover_color = "#000000FF"
    style.nvl_menu_choice_button.idle_background = "#404040CC"
    style.nvl_menu_choice_button.hover_background = "#404040EE"

    style.nvl_window.background = "nvl_window.png"
    style.nvl_menu_choice_button.left_margin = 300
    style.nvl_menu_choice_button.right_margin = 100

init python:
    def toString(num):
        string = format(num, ",")
        return string

screen stats(money,happy,age,income,tax,rent,livingCost,overheadCost,healthCost):
    $ expence = tax + rent + livingCost + overheadCost + healthCost

    $ money = toString(money)
    $ happy = toString(happy)
    $ age = toString(age)
    $ income = toString(income)
    $ expence = toString(expence)

    mousearea:
        area(0,0,0.24,0.225)
        hovered Show("expInfo", transition=dissolve)
        unhovered Hide("expInfo", transition=dissolve)
    frame:
        xalign 0.0 yalign 0.0
        vbox:
            text "Funds:       [money]"
            text "Happiness: [happy]"
            text "Age:           [age]\n"
            text "Annual Income:    [income] "
            text "Annual Expenses: [expence]"


screen expInfo():
    frame:
        xalign 0.3 yalign 0.0
        vbox:
            text "--Expense Sources--\n"
            text "Living:[livingCost]"
            text "Health costs: [healthCost]"
            text "Tax:[tax]"
            text "Rent:[rent]"
            text "Over-head:[overheadCost]"


image Emotion = ConditionSwitch(
    "happy >=30","Face-Smile-Background.png",
    "happy >=10","Face-Neutral-Background.png",
    "happy <10","Face-Sad-Background.png")

init python:
    def deduceTax(pay):
        tax = 0
        bound = 0
        while highBound[bound] != "and above" and bound < 5:
            if pay > int(lowBound[bound]) and pay < int(highBound[bound]):
                tax = pay * (float(rate[bound])/100)
                break
            bound = bound + 1
        if highBound[bound] == "and above":
            tax = tax = pay * (float(rate[bound])/100)
        return tax

init python: #Proceed life until an event is necessary
    import random

    def TimeSkip(age,money,income,AffordHouse,CannotAfford,Promotion,Death,Metspouse,Retire,AfforHouse,Healthy,Emergency,healthCost):
        expence = tax + rent + livingCost + overheadCost + healthCost
        timeSkip = 0

        #Re-set Flags
        CannotAfford = False
        Promotion = False

        while (True): #Check funds
            timeSkip += 1
            money = money + income - expence

            if((money + income) < (expence * 3)): #Thinking for the next 3 years
                CannotAfford = True
                break

            if((promotionProb * (1 + (social/100))) > random.uniform(0,1)): #Promotion chance random, but affected by social
                Promotion = True
                break

            if((jobDanger / 100) > random.uniform(0,1)): #Promotion chance random, but affected by social
                Death = True
                break

            if( not Metspouse and (age + timeSkip >= 30)):  #Find spouse at 30
                Metspouse = True
                break

            if(age > 50 and Healthy):  #Find spouse at 30
                Healthy = False
                break

            if(age + timeSkip >= 65):
                Retire = True
                break

            if(0.2 >= random.uniform(0,1)):  #20% chance of new emergency per year
                Emergency = True
                break

            if(not AffordHouse and money > 400000 + expence):
                AffordHouse = True
                break

        return timeSkip,AffordHouse,CannotAfford,Promotion,Death,Metspouse,Retire,AffordHouse,Healthy,Emergency #Return time skip and flags

label start:

    #Private variables
    $ social = 10
    $ responsible = 30
    $ kids = 0
    $ promotionProb = 0.08
    $ rent = 0
    $ tax = 0
    $ livingCost = 0
    $ overheadCost = 0
    $ jobDanger = 0
    $ healthCost = 0

    #Public variables
    $ money = 1000
    $ happy = 50
    $ age = 18
    $ income = 0
    $ expence = tax + rent + livingCost + overheadCost + healthCost

    $ youthExpence = 300 #including asking parents for money to go out
    $ adultExpence = 3500
    $ elderAdultExpence = 5000

    #Flags
    $ Degree = False
    $ Masters = False
    $ PHD = False
    $ Emlpoyed = False
    $ Metspouse = False
    $ Married = False
    $ Healthy = True
    $ MarrageEventFinish = False
    $ HealthEventFinish = False
    $ Promotion = False
    $ CannotAfford = False #paying rent
    $ MovedOut = False
    $ AffordHouse = False
    $ HouseEventFinish = False
    $ EvadeTax = False
    $ Emergency = False
    $ Retire = False
    $ Death = False

    $ Slacker = False
    $ FriendsFirst = False

    $ Data = Data
    nvl show dissolve
    warn "{cps=20}Proceed through the dialogue by clicking on empty space of the screen or by pressing enter{/cps}"

    nvl clear
    nvl hide dissolve

    pause 1.0

    "{cps=25}Always remember that self sufficiency...{p=5}
    ...Must start with you...{p=5}
    ...And finish with you...{/cps}"

    scene classroom
    play sound "bgm.mp3" loop

    nvl clear
    "Ah yes I remember those days...{p=1.5}\n I'd finally gotten my A levels and had the world ahead of me "
    cr "I think I've heard of you before!{p=1.5}What is your name?\n\n--Click again to enter name--"
    python:
        name = renpy.input("Ah yes my name is...")
        name = name.strip() or "Me"

    define pl = Character("[name]",who_font="SUBWT___.ttf")

    cr "Oh sorry about that!{p=1.5}I think I got the wrong person"

    cr "Never mind that{p=1.5}Tell us about your story"

    pl "Yes, it was back when I was 18 years old..."

    $ livingCost = youthExpence
    show screen stats(money,happy,age,income,tax,rent,livingCost,overheadCost,healthCost)
    show Emotion at left


    pl "{cps=20}Finally! school is over and I have my A Levels!{/cps}"

    pl "{cps=20}My parents don't mind me staying with them a bit longer, but I don't know what to do next...{/cps}"

    nvl show dissolve
    nvl clear
    nar "You choose what happens next!\n Click a below option to act on an option!"

    menu (nvl=True):
        "...Maybe I should get into university and get my degree":
            jump degree

        "...I should just get myself a job and start working":
            jump immediateJob

        "...It's been tough and I deserve a break...I'll think about it after I rest":
            jump lazy


    label degree:   #chose to get degree
        $ Degree = True
        $ age = age + 3
        $ happy = happy - 20
        $ responsible = responsible + 50
        show screen stats(money,happy,age,income,tax,rent,livingCost,overheadCost,healthCost)

        nvl show dissolve

        nvl clear
        nar "{cps=30}3 years have passed, and you got the degree you wanted{/cps}"

        pl "{cps=20} That was a lot harder than I imagined, but I really did it, I got my degree!{/cps}"
        pl "{cps=20} I already got so many job offers I don't even know what to do!{/cps}"

        menu (nvl=True):
            "...This job seems easy! I'll go for this one":
                jump badJob

            "...This job seems challenging, but a good pay":
                jump goodJob

            "...I can study a bit more and get my Masters" if age < 25:
                jump masters

    label masters:
        $ Masters = True
        $ age = age + 2
        $ happy = happy -10
        $ responsible = responsible + 40
        show screen stats(money,happy,age,income,tax,rent,livingCost,overheadCost,healthCost)

        nar "{cps=30}2 more years have passed, and you got your masters{/cps}"

        pl "{cps=20} That was definitely more difficult than the degree, but not as bad as I expected{/cps}"
        pl "{cps=20} I wonder what to do next{/cps}"

        menu (nvl=True):
            "...This job has a good pay and its not so difficult":
                jump goodJob

            "...This job might be a bit tricky, but it has an amazing pay!":
                jump greatJob

            "...I should keep going and get my PHD!" if age < 27:
                jump phd


        jump choice_done

    label phd:
        $ PHD = True
        $ happy = happy - 30
        $ age = age + 6
        $ responsible = responsible + 30
        $ money = money + 10000
        show screen stats(money,happy,age,income,tax,rent,livingCost,overheadCost,healthCost)

        nvl clear
        nar "{cps=30}You applied for your PHD but where told by your parents that if you where to stay in the house you must work{/cps}"
        nar "{cps=30}You saved up 10,000 from part time lecturing while you did your PHD{/cps}"
        nar "{cps=30}6 years have passed, and you got your PHD{/cps}"

        pl "{cps=20} I am now officially a doctor in my subject!{/cps}"
        pl "{cps=20} There arent as many Jobs as I remember though{/cps}"

        menu (nvl=True):
            "...This job is below my level, but it still pays well":
                jump goodJob

            "...I can go above others and straight to a high position in this company":
                jump overQualified

    label lazy:

        $ age = age + 3
        $ responsible = responsible - 25
        $ money = money - 450
        show screen stats(money,happy,age,income,tax,rent,livingCost,overheadCost,healthCost)

        nvl clear
        nar "{cps=30}3 years had gone by while living at your parents' house{/cps}"
        nar "{cps=30}you still earned pocket money from helping around the house and spent it responsibly when going out with friends{/cps}"

        pl "{cps=20} 3 years have passed already. What on earth am I doing?!{/cps}"
        pl "{cps=20} My parents are clearly not happy with me, I should make my choice now{/cps}"

        menu (nvl=True):
            "...I should get straight to work":
                jump immediateJob

            "...I could ask my parents to support me a bit longer to get my degree":
                nvl clear
                nvl hide dissolve
                pl "{cps=20}Wow! I wasn't expecting them to actually agree!{p=1}I'll be sure not to disapoint them{/cps}"
                pause 1.5
                jump degree

        jump immediateJob

    label immediateJob:

        $ age = age + 1
        $ responsible = responsible + 5
        show screen stats(money,happy,age,income,tax,rent,livingCost,overheadCost,healthCost)

        nvl clear
        nar "{cps=30}You spent a year looking for jobs, sent a lot of CVs and finally got selected after an interview{/cps}"

        pl "{cps=20}It's not what I had in mind but I guess this will do{/cps}"

        jump badJob

    label badJob:

        $ happy = happy - 15
        $ income = 9500 #Malta minimum wage
        $ tax = deduceTax(income)
        show screen stats(money,happy,age,income,tax,rent,livingCost,overheadCost,healthCost)

        boss "{cps=20}Who are you and what are you doing here?{/cps}"
        boss "{cps=20}Ah wait!{/cps}"
        boss "{cps=20}I think someone said they found someone to handle that job, is that you?{/cps}"

        pl "{cps=20}y- yes! that's me{/cps}"

        boss "{cps=20}Well I'm busy right now, so find something to do and stop standing around!!{/cps}"

        jump newJob

    label goodJob:
        $ happy = happy + 5
        $ income = 17000
        $ tax = deduceTax(income)
        show screen stats(money,happy,age,income,tax,rent,livingCost,overheadCost,healthCost)

        boss "{cps=20}Sorry I'm late, I almost forgot you were starting today{/cps}"
        boss "{cps=20}What is your name?{/cps}"

        if  name != "Me":
            pl "{cps=20}My name is [name], I look forward to working with you{/cps}"
        else:
            pl "{cps=20}Nice to meet you sir, I look forward to working with you{/cps}"

        if name != "Me":
            boss "{cps=20}Nice to meet you [name]{/cps}"
        else:
            boss "{cps=20}The pleasure is all mine{/cps}"

        jump newJob

    label greatJob:
        $ happy = happy + 40
        $ income = 28000
        $ tax = deduceTax(income)
        show screen stats(money,happy,age,income,tax,rent,livingCost,overheadCost,healthCost)

        if name != "Me":
            boss "{cps=20}Welcome [name]! we've been wanting to finally meet you{/cps}"
        else:
            boss "{cps=20}Welcome! we've been wanting to finally meet you {/cps}"

        boss "{cps=20}Please, let me show you around and introduce you to everyone!{/cps}"

        pl "{cps=20}Thank you so much for the warm welcome, I look forward to working with you{/cps}"

        jump newJob

    label overQualified:

        $ happy = happy - 5
        $ income = 35000
        $ tax = deduceTax(income)
        show screen stats(money,happy,age,income,tax,rent,livingCost,overheadCost,healthCost)
        scene workplace2

        boss "{cps=20}Hello how may I help you?{/cps}"

        pl "{cps=20}Yes, I am here on my first day of work and was hoping someone could show me around{/cps}"

        boss "{cps=20}oh yes, you will be working alone over there{/cps}"
        boss "{cps=20}Go ahead and call people to you when you need something{/cps}"

        pl "{cps=20}Will anyone be showing me what I should do?{/cps}"

        boss "{cps=20}I trust you shall have no problems with your qualifications...{/cps}"

        jump newJob

    label newJob:
        scene workplace
        show Emotion at left

        nvl clear
        nar "You have started your new Job and are receiving  income"

        pl "{cps=20}let's see...{/cps}"
        pl "{cps=20}How should I treat this Job...{/cps}"

        menu (nvl=True):
            "My life isn't about working; I should just relax whenever I can!":
                $ responsible  = responsible - 20
                $ Slacker = True

            "Now that I am working, I should put in as much effort as I can to my work":
                $ happy = happy -10
                $ responsible = responsible + 10
                show screen stats(money,happy,age,income,tax,rent,livingCost,overheadCost,healthCost)

        pl "{cps=20}Now that I have a job, I am getting an income!{/cps}"

        menu (nvl=True):
            "I'll be sure to treat my friends and colleagues to drinks on weekends!":
                $ FriendsFirst = True
                $ happy = happy + 10
                $ overheadCost = (income * 0.3) #Spend a third of salary on friends
                $ social = social + 50
                show screen stats(money,happy,age,income,tax,rent,livingCost,overheadCost,healthCost)

            "I'll be sure to save as much money as I can for a rainy day":
                $ FriendsFirst = False
                $ overheadCost = 0

        if MovedOut:
            jump mainAction


    label SearchPlace:

        pl "{cps=20}Should I try finding my own place?{/cps}"
        menu (nvl=True):
            "Now that I am working, I can just keep living with my parents...":
                jump kickedOut
            "I should save up a bit to buy my own property...":
                jump kickedOut
            "I should find a place to stay and leave my parents in peace...":
                jump findPlace

    label kickedOut:
        $ age = age + 5
        $ expence = tax + rent + livingCost + overheadCost + healthCost
        $ money = money + (income * 5) - (expence * 5)
        show screen stats(money,happy,age,income,tax,rent,livingCost,overheadCost,healthCost)

        nvl clear
        nar "you spend 5 years living with your parents and they think it's time you find your own space"
        nar "They give you one more year to find a place in which you will need to pay rent"

    label findPlace:
        $ age = age + 1
        $ expence = tax + rent + livingCost + overheadCost + healthCost
        $ money = money + (income - expence)
        show screen stats(money,happy,age,income,tax,rent,livingCost,overheadCost,healthCost)



        nar "You spend a year searching for a new place to live and find a few options"

        $ livingCost = 4800
        $ healthCost = 250
        show screen stats(money,happy,age,income,tax,rent,livingCost,overheadCost,healthCost)
        nar "The cost of food and water is 450 per month in Malta, but you can manage to get by on 400"

        pl "{cps=20}These options look good but I'm not sure which to go for...{/cps}"
        menu (nvl=True):
            "The cheap run-down apartment... - 6000 p/year (500 p/month)":
                $ rent = 6000
                $ happy = happy - 10

            "The expensive but comfortable apartment... -12,000 p/year (1000 p/month)":
                $ rent = 12000
                $ happy = happy + 20

        $ MovedOut = True
        show screen stats(money,happy,age,income,tax,rent,livingCost,overheadCost,healthCost)




    #Start Skipping time until event
    label mainAction:
        python:
            timeSkip,AffordHouse,CannotAfford,Promotion,Death,Metspouse,Retire,AffordHouse,Healthy,Emergency = TimeSkip(age,money,income,AffordHouse,CannotAfford,Promotion,Death,Metspouse,Retire,AffordHouse,Healthy,Emergency,healthCost)
            age = age + timeSkip
            expence = tax + rent + livingCost + overheadCost + healthCost
            money = money + (income * timeSkip) - (expence * timeSkip)
        nvl clear
        show screen stats(money,happy,age,income,tax,rent,livingCost,overheadCost,healthCost)
        nar "You have continued your life for [timeSkip] years"

        if(CannotAfford):
            jump cannotAfford

        if(Promotion):
            jump opportunity

        if(Metspouse and not MarrageEventFinish):
            $ MarrageEventFinish = True
            jump findspouse

        if(AffordHouse and not HouseEventFinish):
            $ HouseEventFinish = True
            jump buyHouse

        if(not Healthy and not HealthEventFinish):
            $ HealthEventFinish = True
            jump gotOlder

        if(Emergency):
            jump emergency

        if(Retire):
            jump retirement

        if(Death):
            jump passedAway


        jump mainAction



    label cannotAfford:
        nvl clear
        nar "You notice that with your current situation you won't be able to support yourself and need to think of a solution"

        pl "{cps=20}I'd rather not be thrown out in the streets, so I'd better think of a solution and quickly{/cps}"

        menu (nvl=True):
            "I should move into the cheaper place instead" if rent > 6000:
                $ rent = 6000
                $ happy = happy -35

            "I should look for a better Job":
                jump getBetterJob

            "I'll avoid paying tax, that's my money after all" if not EvadeTax:    #Will eliminate pension later
                $ EvadeTax = True
                $ tax = 0

        show screen stats(money,happy,age,income,tax,rent,livingCost,overheadCost,healthCost)
        jump mainAction

    label getBetterJob:

        pl "{cps=25}Let's see... what kind of jobs can I apply for...{/cps}"

        nvl clear
        menu (nvl=True):
            "...This job has the same hourly rate, but I can work longer hours" if not Degree and not income >= 11000:
                $ income = 11000
                $ expense = (income * 0.15)
                $ happy = happy - 25
                $ social = social -15

            "...This job is very dangerous, but I get paid a lot more for the same hours" if not Degree and not income >=20000:
                $ income = 20000
                $ jobDanger = 20 #20% of death per year

            "...Maybe I should take this more challenging job after all" if Degree and income < 17000:
                jump goodJob

            "...I should study part time for a masters and somehow try to get by until then" if Degree and not Masters:
                jump masters

            "...Maybe I should take this more challenging job after all" if Masters and income < 28000:
                jump greatJob

            "...I should study part time for a PHD and somehow try to get by until then" if Masters and not PHD:
                jump phd

            "...I should go for that high position after all" if PHD and income < 17000:
                jump overQualified

            "Actually, never mind, my current Job will do":
                jump cannotAfford

        show screen stats(money,happy,age,income,tax,rent,livingCost,overheadCost,healthCost)
        jump newJob

    label opportunity:
        nvl clear
        nar "Your boss has been hearing good things about you and offered you a promotion"

        boss "{cps=25}Things will get a little more busy for you, but I promise it will be worth it{/cps}"


        if PHD:
            nar "Boss: {cps=25}Will you accept a raise of 8000 for a little bit of extra effort?{/cps}"
            menu (nvl=True):
                "Yes! I gratefully accept this generous opportunity!":
                    scene workplace2
                    $ income = income + 8000
                    $ happy = happy - 5
                    $ social = social -5

                "I am so sorry for having to refuse your generous offer, but I cannot accept":
                    nar "Boss: {cps=25}I see... hopefully there will be another time an opportunity arises{/cps}"

        elif Masters:
            nar "Boss: {cps=25}Will you accept a raise of 5000 for a little bit of extra effort?{/cps}"
            menu (nvl=True):
                "Yes! I gratefully accept this generous opportunity!":
                    scene workplace2
                    $ income = income + 5000
                    $ happy = happy - 5
                    $ social = social -5

                "I am so sorry for having to refuse your generous offer, but I cannot accept":
                    nar "Boss: {cps=25}I see... hopefully there will be another time an opportunity arises{/cps}"

        elif Degree:
            nar "Boss: {cps=25}Will you accept a raise of 3000 for a little bit of extra effort?{/cps}"
            menu (nvl=True):
                "Yes! I gratefully accept this generous opportunity!":
                    scene workplace2
                    $ income = income + 3000
                    $ happy = happy - 5
                    $ social = social -5

                "I am so sorry for having to refuse your generous offer, but I cannot accept":
                    nar "Boss: {cps=25}I see... hopefully there will be another time an opportunity arises{/cps}"

        else:
            nar "Boss: {cps=25}Will you accept a raise of 1000 for a little bit of extra effort?{/cps}"
            menu (nvl=True):
                "Yes! I gratefully accept this generous opportunity!":
                    $ income = income + 1000
                    $ happy = happy - 5
                    $ social = social -5

                "I am so sorry for having to refuse your generous offer, but I cannot accept":
                    nar "Boss: {cps=25}I see... hopefully there will be another time an opportunity arises{/cps}"
        show screen stats(money,happy,age,income,tax,rent,livingCost,overheadCost,healthCost)
        $ Promotion = False
        jump mainAction

    label findspouse:
        nar "You and a partner you met some time ago have gotten very close and are considering getting married..."

        pl "{cps=25}I don't know what I should do... Should I commit to this person for the rest of my life...?{/cps}"

        menu (nvl=True):
            "I love this person! My life will be better with them in it!":
                $ Married = True
                $ happy = happy + 50
                $ social = social - 10
                sp "I am so happy I wish this moment with you could last forever!"
                pl "{cps=25}Me too{/cps}"
                pl "{cps=25}let's fill our lives with this happiness{/cps}"

            "I don't have time for commitments, my life is my own and I don't need anyone!":
                $ Married = False
                pn "don't worry, I understand... I don't want to be a bother to you"
                pl "{cps=25}I'm sorry, it's not you it's me{/cps}"
                pl "{cps=25}I'm not the kind of person willing to enter such commitments{/cps}"

        $ Metspouse = True

        jump mainAction

    label buyHouse:
        nvl clear
        nar "You have saved enough to buy a house"

        pl "{cps=25}oh wow! I really like this house and it only costs 400,000. I have enough for it!{/cps}"

        menu (nvl=True):
            "I should buy it so that I don't have to pay rent anymore":
                $ money = (money - 400000)
                $ rent = 0
                $ happy = happy + 35
                $ rent = 0
                show screen stats(money,happy,age,income,tax,rent,livingCost,overheadCost,healthCost)
                ll "{cps=25}It's a shame to see you go, but to tell you the truth... you are better off this way{/cps}"
                jump mainAction

            "I'd rather stay at my apartment. I should have enough to pay if off for a while":
                jump mainAction
    label emergency:
        $ Emergency = False
        nar "An unexpected problem in the house had occurred and caused you to lose 1000 to resolve it"
        $ money = money - 1000

        jump mainAction

    label gotOlder:
        nvl clear
        nar "You start to notice that your back and knees don't work as they used to and that your health costs have risen"
        $ healthCost = 2500
        jump mainAction

    label error:
        nar "A problem was reached, and you should not be here"
        pause 10
        jump error

    label retirement:
        stop sound
        nvl clear
        hide Emotion dissolve
        hide screen stats
        if Married:
            $ livingCost = 1600
            $ healthCost = 12000
        else:
            $ livingCost = 800
            $ healthCost = 8000
        nar "{cps=10}You have reached the age of 65 and retire{/cps}\n{cps=10}Your savings: [money]{/cps}"
        if EvadeTax:
            nar "{cps=10}Because of your tax evasion you are not legible for pension and have an income of 0{/cps}"
        else:
            if Married:
                nar "{cps=10}Your new pay: 16,800 in pension for you and your spouse{/cps}"
            else:
                nar "{cps=10}Your new pay: 8400 in pension{/cps}"
        nar "{cps=10}Your new cost of living is [livingCost] including new arising health expenses{/cps}"
        if FriendsFirst:
            nar "{cps=10}At your old age you don't go out as often and you are more cautious with your money{/cps}"
        nvl clear
        if rent > 0: #move to cheaper house unless afford till 100
            if (35 * (livingCost) > money): #cannot survive life in place
                if (10 * (livingCost) > money): #cannot survive 15 years to retire
                    nar "{cps=10}You know that you cannot afford rent for much longer and try moving into an old people's home but are considered too healthy to do so...{/cps}"
                    nar "{cps=10}...What will you do now?{/cps}"
                    menu (nvl=True):
                        "...":
                            jump thanksForPlaying
                        "...":
                            jump thanksForPlaying
                else:
                    nar "{cps=10}Knowing that you cannot afford rent for much longer, you try moving into an old people's home and manage to do so at the age of 75{/cps}"
                    nar "{cps=10}You make new friends there and meet people from your youth who you didn't recognize{/cps}"

                    pl "{cps=20}or... I am expecting something like that to happen now that I have retired{/cps}"

                    cr "{cps=22}Are you sure you will be able to support yourself until you enter the old people's home?{/cps}"

                    pl "{cps=0.8}...{/cps}"

                    tc "{cps=20}I really wish I could help you with your situation, but there isn't really much I can do is there?{/cps}{cps=1.5}...{/cps}"
                    pause 2
                    jump thanksForPlaying
            else:
                nar "{cps=10}Despite the increased cost of living because of health issues, your savings are enough for you to keep living in your apartment{/cps}"
                scene classroom
                pl "{cps=20}And that's how I've gotten up till here.{/cps}"
                pl "{cps=20}Any questions?{/cps}"

                cr "{cps=22}Are you sure your life is still secure in case of an emergency? Something could easily happen out of your expectations, cant it?{/cps}"

                if (money - 35 * (rent + 650)) > 60000:
                    pl "{cps=20}Of course{/cps}"
                    pl "{cps=20}I have much more saved up for a rainy day, so unless anything extreme were to happen, I should be safe{/cps}"
                else:
                    pl "{cps=20}All I can say{/cps}{cps=1.5}...{/cps}{cps=20}I hope nothing happens...{/cps}"

                    tc "{cps=20}That isn't a very respectable answer, but in your situation there isn't really much else you can say is there?{/cps}"
                pause 2
                jump thanksForPlaying
        else:
            if (35 * livingCost) > money:
                nar "{cps=10}With the amount of money you make you often go to the bank to make use of your savings, but eventually it proved to not be enough{/cps}"
                nar "{cps=10}You often find at the end of the month that you do not have enough to eat and that you simply have to live with you back-pains and declining vision{/cps}"

                jump thanksForPlaying
            else:
                scene classroom
                pl "{cps=20}And that is my story, I hope it gave you some insight and inspiration for the future{/cps}"
                pl "{cps=20}Any questions?{/cps}"

                cr "{cps=20}...{/cps}"

                if  name != "Me":
                    tc "{cps=20}Thank you very much for your time today [name], I'm sure your talk today has opened the eyes of at least some of the students today{/cps}"
                else:
                    tc "{cps=20}Thank you very much for your time today, I'm sure your talk today has opened the eyes of at least some of the students today{/cps}"
            jump thanksForPlaying

    label passedAway:
        stop sound
        nvl hide dissolve
        pause 2

        nar "{cps=10}While at the workplace one day an accident had occurred and which caused you injury{/cps}"
        nar "{cps=10}The doctors did their best to save you but, but there was nothing they could do{/cps}"

        nar "{cps=10}You pass away at the age of [age]{/cps}"

        jump thanksForPlaying

    label thanksForPlaying:
        us "{cps=25}Thank you for playing our game, we hope you enjoyed it{/cps}"
        pause 3




    #Background change to outside


    pause 2

    return
