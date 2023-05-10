import random


# For some reason, session['questions'].clear() with redirect(url_for('play')) at the end of the play() function
# does not work. It clears session['questions'] with respect to the GET method, but not the POST method.
# That's why I use a global variable counter.


question_1 = "Task 1: Calculate PPV for Test A."
question_2 = "Task 2: Calculate NPV for Test A."
question_3 = "Task 3: Calculate PPV for Test B."
question_4 = "Task 4: Calculate NPV for Test B."
question_5 = "Task 5: Assuming Test A came up positive, what's the updated PPV?"
question_6 = "Task 6: Assuming Test A came up positive, what's the updated NPV?"
question_7 = "Task 7: Assuming Test B came up positive, what's the updated PPV?"
question_8 = "Task 8: Assuming Test B came up positive, what's the updated NPV?"
questions = [question_1, question_2, question_3, question_4, question_5, question_6, question_7, question_8]
s = None

DATA = {}
for n in range(1, 5):

    prevalence = round(random.uniform(0.1, 0.5), 1)
    absence = 1 - prevalence

    test1_sensitivity = round(random.uniform(0.5, 0.9), 1)
    test1_specificity = round(random.uniform(0.5, 0.9), 1)

    test2_sensitivity = round(random.uniform(0.5, 0.9), 1)
    test2_specificity = round(random.uniform(0.5, 0.9), 1)

    exercise = f"Some population is being examined. There are two tests for a disease (C). " \
               f"Its prevalence is equal to {prevalence}. " \
               f"Test A has a sensitivity of {test1_sensitivity} and a specificity of {test1_specificity}. " \
               f"Test B has a sensitivity of {test2_sensitivity} and a specificity of {test2_specificity}. " \
               f"Round all you answers to two decimals. Your input must be a float or an integer."

    # Remainder.
    # False positive rate, type I error, i.e. alpha.
    # False negative rate, type II error, i.e. beta.

    tpr_1 = test1_sensitivity
    fnr_1 = 1 - test1_sensitivity
    tnr_1 = test1_specificity
    fpr_1 = 1 - test1_specificity

    tpr_2 = test2_sensitivity
    fnr_2 = 1 - test2_sensitivity
    tnr_2 = test2_specificity
    fpr_2 = 1 - test2_specificity

    ppv_1 = tpr_1 * prevalence / (tpr_1 * prevalence + fpr_1 * absence)
    npv_1 = tnr_1 * absence / (tnr_1 * absence + (fnr_1 * prevalence))

    ppv_2 = tpr_2 * prevalence / (tpr_2 * prevalence + fpr_2 * absence)
    npv_2 = tnr_2 * absence / (tnr_2 * absence + (fnr_2 * prevalence))

    # Calculate confusion matrix A x C.
    # true positive   (tp)       false positive  (fp)
    # false negative  (fn)       true negative   (tn)

    tp_1 = tpr_1 * prevalence
    fn_1 = fnr_1 * prevalence
    tn_1 = tnr_1 * absence
    fp_1 = fpr_1 * absence

    # Calculate confusion matrix B x C.

    tp_2 = tpr_2 * prevalence
    fn_2 = fnr_2 * prevalence
    tn_2 = tnr_2 * absence
    fp_2 = fpr_2 * absence

    # After Test A. What's the procedure? We're now in the group which tested A-positive. We assume that B's sensitivity
    # (true positive rate) and specificity (true negative rate) remain the same in this group. In A, the new prevalence
    # of the disease is equal to A's PPV:

    prevalence_in_A = ppv_1
    absence_in_A = 1 - ppv_1

    # How many people are in A? P(A), i.e. the denominator of A's PPV, which is:

    population_A = tp_1 + fp_1
    total_with_condition_in_A = population_A * prevalence_in_A
    total_without_condition_in_A = population_A * absence_in_A

    # Now, within A, we need to calculate confusion matrix B x C:

    tp_test_B_in_A = total_with_condition_in_A * tpr_2
    fn_test_B_in_A = total_with_condition_in_A * fnr_2
    tn_test_B_in_A = total_without_condition_in_A * tnr_2
    fp_test_B_in_A = total_without_condition_in_A * fpr_2

    # Calculate PPV for Test B given A. Calculate NPV for Test B given A.

    ppv_test_B_in_A = tp_test_B_in_A / (tp_test_B_in_A + fp_test_B_in_A)
    npv_test_B_in_A = tn_test_B_in_A / (tn_test_B_in_A + fn_test_B_in_A)

    # Now we are writing an analogous code. We are after positive Test B. We assume that A's sensitivity and specificity
    # remain the same in this group.

    prevalence_in_B = ppv_2
    absence_in_B = 1 - ppv_2

    population_B = tp_2 + fp_2
    total_with_condition_in_B = population_B * prevalence_in_B
    total_without_condition_in_B = population_B * absence_in_B

    tp_test_A_in_B = total_with_condition_in_B * tpr_1
    fn_test_A_in_B = total_with_condition_in_B * fnr_1
    tn_test_A_in_B = total_without_condition_in_B * tnr_1
    fp_test_A_in_B = total_without_condition_in_B * fpr_1

    ppv_test_A_in_B = tp_test_A_in_B / (tp_test_A_in_B + fp_test_A_in_B)
    npv_test_A_in_B = tn_test_A_in_B / (tn_test_A_in_B + fn_test_A_in_B)

    # Correct answers, rounded, for all questions.

    ppv_1 = round(ppv_1, 2)
    npv_1 = round(npv_1, 2)

    ppv_2 = round(ppv_2, 2)
    npv_2 = round(npv_2, 2)

    ppv_test_B_in_A = round(ppv_test_B_in_A, 2)
    npv_test_B_in_A = round(npv_test_B_in_A, 2)

    ppv_test_A_in_B = round(ppv_test_A_in_B, 2)
    npv_test_A_in_B = round(npv_test_A_in_B, 2)

    # Saving data:

    DATA[n] = [exercise, ppv_1, npv_1, ppv_2, npv_2, ppv_test_B_in_A, npv_test_B_in_A, ppv_test_A_in_B, npv_test_A_in_B]

# for i in DATA:
#     print(DATA[i])
