from pathlib import Path
from matcher import read, get_answer, load_bot

id_dataset, df, training_matrix, vectorizer = load_bot()
def evaluate(vectorizer, training_matrix, questions_dataset, id_dataset, df):
    threshold_score = [0.1,0.2,0.3,0.4,0.5]

    for t in threshold_score:
        correct = 0
        wrong_FAQ = 0
        wrongly_refused = 0
        correctly_refused = 0
        wrongly_answered = 0
        total_test_questions = 0
        lang = {"english": 0,
                "urdu": 0}
        test_type = {"paraphrase_english": 0,
                        "roman_urdu": 0,
                        "short/typo": 0,
                        "indirect/scenario":  0,
                        "out_of_scope": 0,
                        "related_but_not_covered": 0}
            
        test_type_total = {"paraphrase_english_total": 0,
                    "roman_urdu_total": 0,
                    "short/typo_total": 0,
                    "indirect/scenario_total":  0,
                    "out_of_scope_total": 0,
                    "related_but_not_covered_total": 0}

        lang_total = {"english_total": 0,
                    "urdu_total": 0}
        
        for key, value in questions_dataset.iterrows():
            passed = False
            total_test_questions = total_test_questions + 1
            ans =  get_answer(vectorizer, training_matrix, value["test_question"], value["lang"], id_dataset, df, t)

            if value["test_type"] == "Paraphrase (English)":
                test_type_total["paraphrase_english_total"] += 1
            elif value["test_type"] == "Roman Urdu":
                test_type_total["roman_urdu_total"] += 1
            elif value["test_type"] == "Short / typo":
                test_type_total["short/typo_total"] += 1
            elif value["test_type"] == "Indirect / scenario":
                test_type_total["indirect/scenario_total"] += 1
            elif value["test_type"] == "Out of scope":
                test_type_total["out_of_scope_total"] += 1
            else:
                test_type_total["related_but_not_covered_total"] += 1

            if value["lang"] == "english":
                lang_total["english_total"] += 1
            else:
                lang_total["urdu_total"] += 1

            id_result = None
            if value["expected_faq_id"] != "NONE":
                if int(value["expected_faq_id"]) ==  ans["id"]:
                    id_result = True
                else:
                    id_result = False
        
            if value["expected_faq_id"] == "NONE":
                if ans["id"] == 0:
                    # print('ID is "NONE"')
                    # print(f"Expected ID: {value["expected_faq_id"]}")
                    # print("Test case passed")
                    # print(f"Test question: {value["test_question"]}")
                    # print("Correctly refused")
                    # print(f"Score: {ans["score"]}")
                    # print("------")
                    correctly_refused = correctly_refused + 1
                    passed = True
                else:
                    # print('ID is "NONE"')
                    # print(f"Expected ID: {value["expected_faq_id"]}")
                    # print("Test case failed")
                    # print(f"Test question: {value["test_question"]}")
                    # print("wrongly answered")
                    # print(f"Score: {ans["score"]}")
                    # print("------")
                    wrongly_answered = wrongly_answered + 1  
            elif id_result == True:
                # print("Expected ID matched")
                # print(f"Expected ID: {value["expected_faq_id"]}")
                # print("Test case passed")
                # print(f"Test question: {value["test_question"]}")
                # print("correct")
                # print(f"Score: {ans["score"]}")
                # print("------")
                correct = correct + 1
                passed = True
            else:
                if ans["id"] == 0:
                    # print("Expected ID not matched")
                    # print(f"Expected ID: {value["expected_faq_id"]}")
                    # print("Test case failed")
                    # print(f"Test question: {value["test_question"]}")
                    # print("wrongly refused")
                    # print(f"Score: {ans["score"]}")
                    # print("------")
                    wrongly_refused = wrongly_refused + 1
                else:
                    # print("Expected ID not matched")
                    # print(f"Expected ID: {value["expected_faq_id"]}")
                    # print("Test case failed")
                    # print(f"Test question: {value["test_question"]}")
                    # print("wrong FAQ")
                    # print(f"Score: {ans["score"]}")
                    # print("------")
                    wrong_FAQ = wrong_FAQ + 1

            if passed == True:
                if value["test_type"] == "Paraphrase (English)":
                    test_type["paraphrase_english"] = test_type["paraphrase_english"] + 1
                elif value["test_type"] == "Roman Urdu":
                    test_type["roman_urdu"] = test_type["roman_urdu"] + 1
                elif value["test_type"] == "Short / typo":
                    test_type["short/typo"] = test_type["short/typo"] + 1
                elif value["test_type"] == "Indirect / scenario":
                    test_type["indirect/scenario"] = test_type["indirect/scenario"] + 1
                elif value["test_type"] == "Out of scope":
                    test_type["out_of_scope"] = test_type["out_of_scope"] + 1
                else:
                    test_type["related_but_not_covered"] = test_type["related_but_not_covered"] + 1

                if value["lang"] == "english":
                    lang["english"] = lang["english"] + 1
                else:
                    lang["urdu"] = lang["urdu"] + 1


        overall_accuracy = ((correctly_refused + correct) / total_test_questions) * 100
        answerable_accuracy = correct / (correct + wrong_FAQ + wrongly_refused) * 100
        Of_topic_accuracy = correctly_refused / (correctly_refused + wrongly_answered) * 100
        test_type_english = test_type["paraphrase_english"] / test_type_total["paraphrase_english_total"] * 100
        test_type_urdu = test_type["roman_urdu"] / test_type_total["roman_urdu_total"] * 100
        test_type_typo = test_type["short/typo"] / test_type_total["short/typo_total"] * 100
        test_type_scenario = test_type["indirect/scenario"] / test_type_total["indirect/scenario_total"] * 100
        test_type_outOfScope = test_type["out_of_scope"] / test_type_total["out_of_scope_total"] * 100
        test_type_related = test_type["related_but_not_covered"] / test_type_total["related_but_not_covered_total"] * 100
        lang_eng = lang["english"] / lang_total["english_total"] * 100
        lang_ur = lang["urdu"] / lang_total["urdu_total"] * 100
        print("")
        print("Accuracy Score by Test Type")
        print(f"English(paraphase): {test_type_english}")
        print(f"Urdu: {test_type_urdu}")
        print(f"Short/Typo: {test_type_typo}")
        print(f"Indirect/Scenario: {test_type_scenario}") 
        print(f"Out of Scope: {test_type_outOfScope}")
        print(f"Related but not covered: {test_type_related}")
        print("---------------------")   

        print("")
        print("Accuracy Score by Language Type")
        print(f"English: {lang_eng}")
        print(f"Urdu: {lang_ur}")
        print("-----------------------")

        print("")
        print("Overall Accuray Score")
        print(f"Overall Accuracy: {overall_accuracy}")
        print(f"Answerable: {answerable_accuracy}")
        print(F"Of-topic accuracy: {Of_topic_accuracy}")
        print("_______________________________________________________")
        print(" ")

testcase = read(Path(__file__).parent / "faq_test_questions_50.csv")
print(testcase.info())
evaluate(vectorizer, training_matrix, testcase, id_dataset, df)