import streamlit as st
import pandas as pd

st.sidebar.title('設定値')
#年齢
start_age = st.sidebar.number_input('ローンを開始する年齢', 25, 100, 28)
end_work_age = st.sidebar.number_input('退職する年齢', 25, 100, 65)
end_age = st.sidebar.number_input('死ぬ年齢(ざっくり)', 65, 120, 85)
#初期貯金額
start_money = st.sidebar.number_input('初期貯金額(万円)', 25, 10000, 500)
#年収関連
start_salary_original = st.sidebar.number_input('年収(万円)※額面', 100, 2000, 400)
start_salary_rate = st.sidebar.number_input('税金で取られる率(%)※通常25%くらい', 0, 40, 25)
start_salary = start_salary_original * (1-start_salary_rate/100) #万円
salary_rate = st.sidebar.number_input('年収の年間上昇率(%)', 0.0, 10.0, 1.0)
retirement_allowance = st.sidebar.number_input('退職金(万円)', 0, 10000, 1500)
#生活費
cost_of_living = st.sidebar.number_input('生活費(万円)', 0, 100, 20)
#教育費
education_per_child = st.sidebar.number_input('子供1人にかかる費用(万円)', 0, 10000, 1600)
number_of_child = st.sidebar.number_input('子供の人数', 0, 5, 2)
first_child_age = st.sidebar.number_input('自分が何歳の時に第1子が産まれるか？(人)', 10, 100, 28)
second_child_age = st.sidebar.number_input('自分が何歳の時に第2子が産まれるか？(人)', 10, 100, 31)
#住宅ローン
down_payment = st.sidebar.number_input('頭金(万円)', 0, 2000, 500)
selling_price = st.sidebar.number_input('住宅販売価格(万円)', 0, 20000, 4000)
first_expense_rate = st.sidebar.number_input('販売価格に対する初期費用(%)', 0, 20, 6)
interest_rate = st.sidebar.number_input('金利', 0.0, 10.0, 1.4)
years = st.sidebar.number_input('ローン年数', 0, 100, 35)
tax = st.sidebar.number_input('固定資産税＋都市計画税(万円)', 0, 200, 17)


#----------住宅ローン-----------#
age_living, money_living_vs_age = [], []
true_down_payment = down_payment - selling_price * first_expense_rate/100
borrowings = selling_price - true_down_payment
year_pay = borrowings/years
for i in range(0, end_age-start_age):
    age_living.append(start_age + i)
    if i < 35:
        rate_price = borrowings * interest_rate/100
        money_living = year_pay + rate_price + tax
        money_living_vs_age.append(money_living)
    else:
        money_living_vs_age.append(0)

df_living = pd.DataFrame([age_living, money_living_vs_age], index=['age', 'money']).T

#----------教育費-----------#
age_education, money_education_vs_age = [], []
education_year = 22 + second_child_age - first_child_age
a = education_per_child*number_of_child*3/education_year**3
for i in range(0, end_age-start_age):
    age_education.append(start_age + i)
    if i <= education_year:
        money_education = a * i**2
        money_education_vs_age.append(money_education)
    else:
        money_education_vs_age.append(0)
df_education = pd.DataFrame([age_education, money_education_vs_age], index=['age', 'money']).T 

#----------生活費-----------#
age_routine, money_routine_vs_age = [], []
for i in range(0, end_age-start_age):
    age_routine.append(start_age + i)
    money_routine_vs_age.append(cost_of_living*12)
df_routine = pd.DataFrame([age_routine, money_routine_vs_age], index=['age', 'money']).T 


df_all_spending = df_living + df_education + df_routine
df_all_spending.iloc[:,0] = df_all_spending.iloc[:,0]/3


#----------所得分-----------#
age_salary, money_salary_vs_age = [], []
salary = start_salary
money = start_money + salary


for i, j in enumerate(range(start_age, end_age)):
    if start_age <= j | j < 65:
        age_salary.append(start_age + i)
        salary = salary + salary*salary_rate/100
        money = money + salary - df_all_spending.iloc[i,1]
        money_salary_vs_age.append(money)
    elif j == 65:
        age_salary.append(start_age + i)
        money = money + retirement_allowance - df_all_spending.iloc[i,1]
        money_salary_vs_age.append(money)
    elif end_work_age < j | j <= end_age:
        age_salary.append(start_age + i)
        money = money - df_all_spending.iloc[i,1]
        money_salary_vs_age.append(money)
df = pd.DataFrame([age_salary, money_salary_vs_age], index=['age', 'money']).T


if st.checkbox('表を表示します(年齢と所持金(万円))'):
    st.write(df)

dat = df.set_index('age')
st.line_chart(dat)