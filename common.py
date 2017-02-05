#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import pickle
import json


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")

def save_data(file, data_list, mode="wb"):
    """
    数据保存到文件中
    :param file: 文件名
    :param data_list: 保存数据
    :param mode: 文件操作模式
    :return:无
    """
    with open(file, mode) as f:
        pickle.dump(data_list, f)


def get_data(file):
    """
    读取文件信息
    :param file: 文件名
    :return:文件内容的数据列表
    """
    with open(file, "rb") as f:
        data_list = pickle.load(f)
    return data_list


def show_pickle_data():
    """
    查看pickle序列化后的数据
    :return:
    """
    import pprint
    _teacher = os.path.join(DB_DIR, "teachers.db")
    _student = os.path.join(DB_DIR, "students.db")
    _file = os.path.join(DB_DIR, "courses.db")
    data = get_data(_file)
    pprint.pprint(data)


def save_data_json(file, data_list, mode="w"):
    """
    数据保存到文件中
    :param file: 文件名
    :param data_list: 保存数据
    :param mode: 文件操作模式
    :return:无
    """
    with open(file, mode) as f:
        for info in data_list:
            f.write(json.dumps(info))
            f.write("\n")


def get_data_json(file):
    """
    读取文件信息
    :param file: 文件名
    :return:文件内容的数据列表
    """
    data_list = []
    with open(file, "r") as f:
        for line in f:
            if line.strip():
                data_list.append(json.loads(line))
        return data_list


class School(object):
    """
    学校类：可招聘老师、创建班级和创建课程
    """
    def __init__(self, name):
        self.name = name

    def hire_teacher(self, name, course, grade=None):
        _file = os.path.join(DB_DIR, "teachers.db")
        if not os.path.exists(_file):
            teacher_list = [{"school": self.name, "teacher": name, "course": course, "grade": grade}]
        else:
            teacher_list =  get_data(_file)
            teacher_list.append({"school": self.name, "teacher": name, "course": course, "grade": grade})
        save_data(_file, teacher_list)

    def create_grade(self, grade, teacher):
        _file = os.path.join(DB_DIR, "teachers.db")
        grade_list = get_data(_file)
        for i in range(len(grade_list)):
            if grade_list[i]["teacher"] == teacher:
                grade_list[i]["grade"] = grade
                save_data(_file, grade_list)
                break

    def create_course(self, course, period, price):
        _file = os.path.join(DB_DIR, "courses.db")
        if not os.path.exists(_file):
            course_list = [{self.name:{"course": course, "period":period, "price":price}}]
        else:
            course_list = get_data(_file)
            course_list.append({self.name:{"course": course, "period":period, "price":price}})
        save_data(_file, course_list)


class Course(object):
    """
    课程类：可查看课程信息
    """
    def __init__(self, name, period, price):
        self.name = name
        self.period = period
        self.price = price

    @staticmethod
    def cat_course(school_obj):
        _file = os.path.join(DB_DIR, "courses.db")
        course_list = get_data(_file)
        print("课程清单".center(60, '*'))
        for info in course_list:
            if school_obj.name in info:
                print("【学校】{:8} 【课程】{:6} 【周期】{:9} 【价格】{:5}".format(
                    school_obj.name, info[school_obj.name]["course"], info[school_obj.name]["period"],
                    info[school_obj.name]["price"]))
        print("end".center(65, "*"))


class Teacher(object):
    """
    讲师类：可选择班级、查看班内学员信息和修改学生成绩
    """
    _teacher = os.path.join(DB_DIR, "teachers.db")
    _student = os.path.join(DB_DIR, "students.db")

    def __init__(self, name, school_obj):
        self.name = name
        self.school = school_obj
        self.exist_flag = False

    def set_grade(self, grade):
        if os.path.exists(Teacher._teacher):
            teacher_list = get_data(Teacher._teacher)
            for i in range(len(teacher_list)):
                if teacher_list[i]["teacher"] == self.name:
                    self.exist_flag = True
                    teacher_list[i]["grade"] = grade
                    save_data(Teacher._teacher, teacher_list)
                    break
            if not self.exist_flag:
                print("\t\033[0;31m目前未招聘%s老师！\033[0m" % self.name)
        else:
            print("\t\033[0;31m目前未招聘%s老师！\033[0m" % self.name)

    def cat_students(self):
        if not os.path.exists(Teacher._teacher):
            print("\t\033[0;31m目前未招聘%s老师！\033[0m" % self.name)
            return
        if not os.path.exists(Teacher._student):
            print("\t\033[0;31m目前没有学生！\033[0m")
            return
        teacher_list = get_data(Teacher._teacher)
        for i in range(len(teacher_list)):
            if teacher_list[i]["teacher"] == self.name:
                self.exist_flag = True
                _grade = teacher_list[i]["grade"]
                break
        if not self.exist_flag:
            print("\t\033[0;31m目前未招聘%s老师！\033[0m" % self.name)
            return

        student_list = get_data(Teacher._student)
        student_exist_flag = False
        for i in range(len(student_list)):
            if student_list[i]["grade"] == _grade:
                student_exist_flag = True
                print("-"*60)
                print("【学校】{:8} 【班级】{:3} 【姓名】{:5} 【缴费】{:5} 【成绩】{:3}".format(
                    student_list[i]["school"], student_list[i]["grade"], student_list[i]["name"],
                    student_list[i]["tuition"], student_list[i]["result"]
                ))
                print("-"*60)

        if not student_exist_flag:
            print("\t\033[0;31m目前%s班没有学生！\033[0m" % _grade)

    def set_result(self, student_name, result):
        if not os.path.exists(Teacher._teacher):
            print("\t\033[0;31m目前未招聘%s老师！\033[0m" % self.name)
            return
        if not os.path.exists(Teacher._student):
            print("\t\033[0;31m目前没有学生！\033[0m")
            return
        teacher_list = get_data(Teacher._teacher)
        for i in range(len(teacher_list)):
            if teacher_list[i]["teacher"] == self.name:
                self.exist_flag = True
                break
        if not self.exist_flag:
            print("\t\033[0;31m目前未招聘%s老师！\033[0m" % self.name)
            return

        student_list = get_data(Teacher._student)
        student_exist_flag = False
        for i in range(len(student_list)):
            if student_list[i]["name"] == student_name:
                student_exist_flag = True
                student_list[i]["result"] = result
                save_data(Teacher._student, student_list)
                print("\t\033[0;32m学生%s的成绩更新成功！\033[0m" % student_name)

        if not student_exist_flag:
            print("\t\033[0;31m目前没有学生%s！\033[0m" % student_name)


class Student(object):
    """
    学员类：可注册、缴费、选择班级
    """

    def __init__(self, name, school_obj):
        self.name = name
        self.school = school_obj
        self.exist_flag = False
        self.tuition = 0
        self.file = os.path.join(DB_DIR, "students.db")

    def enroll(self, grade=None):
        if os.path.exists(self.file):
            student_list = get_data(self.file)
            for i in range(len(student_list)):
                if student_list[i]["name"] == self.name:
                    print("\t\033[0;31m%s 已注册！\033[0m" % self.name)
                    self.exist_flag = True
                    break
            if not self.exist_flag:
                student_list.append({"school":self.school.name, "grade": None,\
                                                        "name": self.name, "tuition":0,"result":0})
        else:
            student_list = [{"school":self.school.name, "grade": None, "name": self.name, "tuition":0,\
                            "result":0}]
        if not self.exist_flag:
            save_data(self.file, student_list)
            print("\t\033[0;32m%s 注册成功！\033[0m" % self.name)

    def pay_tuition(self, money):
        if os.path.exists(self.file):
            student_list = get_data(self.file)
            for i in range(len(student_list)):
               if student_list[i]["name"] == self.name:
                   self.tuition = student_list[i]["tuition"]
                   self.exist_flag = True
                   break

            if self.exist_flag:
                self.tuition += money
                student_list[i]["tuition"] = self.tuition
                save_data(self.file, student_list)
                print("\t\033[0;32m%s 缴费%s元成功！\033[0m" % (self.name, money))
            else:
                print("\t\033[0;31m%s 请先注册！\033[0m" % self.name)
        else:
            print("\t\033[0;31m%s 请先注册！\033[0m" % self.name)


    def set_grade(self, grade):
        if os.path.exists(self.file):
            student_list = get_data(self.file)
            for i in range(len(student_list)):
               if student_list[i]["name"] == self.name:
                   self.exist_flag = True
                   break

            if self.exist_flag:
                student_list[i]["grade"] = grade
                save_data(self.file, student_list)
                print("\t\033[0;32m%s 选择%s班成功！\033[0m" % (self.name, grade))
            else:
                print("\t\033[0;31m%s 请先注册！\033[0m" % self.name)
        else:
            print("\t\033[0;31m%s 请先注册！\033[0m" % self.name)