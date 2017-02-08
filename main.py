#!/usr/bin/env python
# -*- coding:utf-8 -*-

import common
import templates


def manage():
    """
    管理平台
    :return:无
    """
    school_name = input("Enter school name :").strip()
    school_obj = common.School(school_name)
    while True:
        print(templates.manage_menu)
        choice = input(">>>").strip()
        if choice == "1":
            name = input("Enter teacher name: ").strip()
            course = input("Enter course name: ").strip()
            school_obj.hire_teacher(name, course)
        elif choice == "2":
            teacher = input("Enter teacher name: ").strip()
            grade = input("Enter grade name: ").strip()
            school_obj.create_grade(grade, teacher)
        elif choice == "3":
            print("\t请输入课程名称、周期和价格，以“|”分割，例如：linux|7 months|7000")
            course,period,price = input(">>").strip().split("|")
            school_obj.create_course(course, period, price)
            common.Course.cat_course(school_obj)
        elif choice == "4":
            break
        else:
            print("\t\033[0;31m请输入正常选项！\033[0m")
            continue


def teacher():
    """
    讲师中心
    :return:无
    """
    school_name = input("Enter school name: ").strip()
    teacher_name = input("Enter teacher name: ").strip()
    school_obj = common.School(school_name)
    teacher_obj = common.Teacher(teacher_name, school_obj)

    while True:
        print(templates.teacher_menu)
        choice = input(">>").strip()
        if choice == "1":
            grade = input("Enter grade number : ").strip()
            teacher_obj.set_grade(grade)
        elif choice == "2":
           teacher_obj.cat_students()
        elif choice == "3":
            student_name = input("Enter student name :").strip()
            result = input("Enter student result : ").strip()
            teacher_obj.set_result(student_name, result)
        elif choice == "4":
            break
        else:
            print("\t\033[0;31m%s 请输入正常选项！\033[0m" % teacher_obj.name)
            continue


def student():
    """
    学员之家
    :return:无
    """
    school_name = input("Enter school name: ").strip()
    student_name = input("Enter student name: ").strip()
    school_obj = common.School(school_name)
    student_obj = common.Student(student_name, school_obj)

    while True:
        print(templates.student_menu)
        choice = input(">>").strip()
        if choice == "1":
            student_obj.enroll()
        elif choice == "2":
            money = input("Enter tuition : ").strip()
            while not money.isdigit():
                print("\t\033[0;31m%s 请输入正确缴费金额！\033[0m" % student_name)
                money = input("Enter tuition : ").strip()
            student_obj.pay_tuition(int(money))

        elif choice == "3":
            grade = input("Enter grade number : ").strip()
            student_obj.set_grade(grade)
        elif choice == "4":
            break
        else:
            print("\t\033[0;31m%s 请输入正常选项！\033[0m" % student_obj.name)
            continue


def main():
    """
    选课系统
    :return:无
    """
    while True:
        print(templates.first_menu)
        choice = input(">>").strip()
        if choice =="1":
            manage()
        elif choice == "2":
            teacher()
        elif choice == "3":
            student()
        elif choice == "4":
            break
        else:
            print("\t\033[0;31m请输入正常选项！\033[0m")
            continue


if __name__ == '__main__':
    main()