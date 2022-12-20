import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_file, make_response
)
from project.db import(
    get_resident_info_name,get_resident_info_identity,get_resident_info_region,
    get_ill_info_street,get_ill_info_time,get_close_region,medical_if_exists,get_close_location
)
from project.auth import(
    login_required
)
import csv
bp = Blueprint('CDC', __name__)

@bp.route('/CDC/main',methods = ('GET', 'POST'))
@login_required
def CDCmain():
    user_name=session['user_name']
    print("CDC I'm coming!")
    return render_template('CDC/main.html',user_name=user_name)
# 通过姓名、身份证号等查找居民信息，或者浏览某一区域的情况
@bp.route('/CDC/CDCinquire_resident',methods=('GET','POST'))
@login_required 
def CDCinquire_resident():
    user_name=session['user_name']
    if request.method == 'POST':
        name = request.form['name']
        identity = request.form['identity']
        region = request.form['region']
        rtype = request.form['rtype'] 
        print(rtype)
        error = None
        if len(name) == 0 and len(identity) == 0 and (len(region) == 0 or len(rtype)==0):
            error = '请输入所查询信息'
        elif len(identity) == 0 and len(region) == 0 and len(rtype)==0:
            resident_info = get_resident_info_name(name)
        elif len(name) == 0 and len(region) == 0 and len(rtype)==0:
            resident_info = get_resident_info_identity(identity)
        elif len(name) == 0 and len(identity) == 0:
            if(rtype=='1'):
                rtype='street'
            if(rtype=='2'):
                rtype='community'
            print(rtype)
            resident_info = get_resident_info_region(region,rtype)
        else:
            error = '仅可选择一种查询方式,请保持其他输入框空白'
        if error is None:
            length = len(resident_info)
            if(length==0):
                error = '查询结果为空，请检查输入信息'
            else:
                header = ['身份证号','姓名','联系电话','性别','出生日期','居住地','进入居住地时间','离开居住地时间']
                with open('instance/inquire_result.csv','w') as result_file:
                    writer = csv.writer(result_file)
                    writer.writerow(header)
                    for i in range(length):
                        if resident_info[i][7] is None:
                            data = [resident_info[i][0],resident_info[i][1],resident_info[i][2],resident_info[i][3],resident_info[i][4],resident_info[i][5],resident_info[i][6],'暂未离开']
                        else:
                            data = [resident_info[i][0],resident_info[i][1],resident_info[i][2],resident_info[i][3],resident_info[i][4],resident_info[i][5],resident_info[i][6],resident_info[i][7]]
                        writer.writerow(data)
                return render_template('CDC/CDCinquire_resident.html',length=length,resident_info=resident_info,user_name=user_name)  
        flash(error)
    return render_template('CDC/CDCinquire_resident.html',user_name=user_name)

#根据时间范围或地区查询阳性病例
@bp.route('/CDC/CDCinquire_positive',methods=('GET','POST'))
@login_required 
def CDCinquire_positive():
    user_name=session['user_name']
    if request.method == 'POST':
        time_start = request.form['time_start'] 
        time_end = request.form['time_end']
        street = request.form['street']
        error = None
        if len(street)==0:
            if(len(time_end)==0 or len(time_start)==0):
                error='请输入完整的查询信息'
        else:
            if(len(time_end)!=0 or len(time_start)!=0):
                error='请选择一种查询方式，并保证其他输入框空白'
        if error is None:
            if len(street)!=0:
                ill_info = get_ill_info_street(street)
            else:
                ill_info = get_ill_info_time(time_start,time_end)
            length = len(ill_info)
            if(length==0):
                error = '未查询到阳性病例'
            else:
                header = ['身份证号','姓名','联系电话','性别','出生日期','居住地','进入居住地时间','离开居住地时间']
                with open('instance/inquire_result.csv','w') as result_file:
                    writer = csv.writer(result_file)
                    writer.writerow(header)
                    for i in range(length):
                        if ill_info[i][7] is None:
                            data = [ill_info[i][0],ill_info[i][1],ill_info[i][2],ill_info[i][3],ill_info[i][4],ill_info[i][5],ill_info[i][6],'暂未离开']
                        else:
                            data = [ill_info[i][0],ill_info[i][1],ill_info[i][2],ill_info[i][3],ill_info[i][4],ill_info[i][5],ill_info[i][6],ill_info[i][7]]
                        writer.writerow(data)
                return render_template('CDC/CDCinquire_positive.html',length=length,ill_info=ill_info,user_name=user_name)
        flash(error)
    return render_template('CDC/CDCinquire_positive.html',user_name=user_name) 

#输入病例的检测编号，根据其居住地排查检测时间前后7天与阳性病例居住在同一小区的居民信息
@bp.route('/CDC/CDCinquire_close_region',methods=('GET','POST'))
@login_required
def CDCinquire_close_region():
    user_name=session['user_name']
    if request.method == 'POST':
        test_id = request.form['test_id']
        error = None
        if_exists = medical_if_exists(test_id)
        if if_exists == False:
            error = '核酸检测编号不存在，请检查后重新输入'
        else:
            close_resident_info = get_close_region(test_id)
            length = len(close_resident_info)
            if(length==0):
                error = '未查询到与该阳性病例前后七天内居住在同一小区的居民'
            else:
                header = ['身份证号','姓名','联系电话','性别','出生日期','居住地','进入居住地时间','离开居住地时间']
                with open('instance/inquire_result.csv','w') as result_file:
                    writer = csv.writer(result_file)
                    writer.writerow(header)
                    for i in range(length):
                        if close_resident_info[i][7] is None:
                            data = [close_resident_info[i][0],close_resident_info[i][1],close_resident_info[i][2],close_resident_info[i][3],close_resident_info[i][4],close_resident_info[i][5],close_resident_info[i][6],'暂未离开']
                        else:
                            data = [close_resident_info[i][0],close_resident_info[i][1],close_resident_info[i][2],close_resident_info[i][3],close_resident_info[i][4],close_resident_info[i][5],close_resident_info[i][6],close_resident_info[i][7]]
                        writer.writerow(data)
                return render_template('CDC/CDCinquire_close_region.html',length=length,close_resident_info=close_resident_info,user_name=user_name)
        flash(error)
    return render_template('CDC/CDCinquire_close_region.html',user_name=user_name)

#输入病例的身份证号以及排查的时间范围，查询与该病例在指定时间范围内存在时空密接的人员
@bp.route('/CDC/CDCinquire_close',methods=('GET','POST'))
@login_required
def CDCinquire_close():
    print(12311111)
    user_name=session['user_name']
    if request.method == 'POST':
        
        identity = request.form['identity']          #identity、begin_time、end_time均为required
        begin_time = request.form['begin_time']
        end_time = request.form['end_time']
        print("haha?")
        error = None
        close_people_info = get_close_location(identity,begin_time,end_time)
        length=len(close_people_info)
        if length == 0:
            error = '未查询到相关信息，请再次检查输入'
        else:
            header = ['身份证号','姓名','联系电话','性别','出生日期','居住地','进入居住地时间','离开居住地时间']
            with open('instance/inquire_result.csv','w') as result_file:
                writer = csv.writer(result_file)
                writer.writerow(header)
                for i in range(length):
                    if close_people_info[i][7] is None:
                        data = [close_people_info[i][0],close_people_info[i][1],close_people_info[i][2],close_people_info[i][3],close_people_info[i][4],close_people_info[i][5],close_people_info[i][6],'暂未离开']
                    else:
                        data = [close_people_info[i][0],close_people_info[i][1],close_people_info[i][2],close_people_info[i][3],close_people_info[i][4],close_people_info[i][5],close_people_info[i][6],close_people_info[i][7]]
                    writer.writerow(data)
            return render_template('CDC/CDCinquire_close.html',length=length,close_people_info=close_people_info,user_name=user_name)
        flash(error)
    return render_template('CDC/CDCinquire_close.html',user_name=user_name)

# 下载查询结果
@bp.route('/CDC/CDCdownload',methods = ('GET', 'POST'))
@login_required
def DBdownload():
    if request.method == 'POST':
        print("why?")
        user_name = session['user_name']
        # return send_from_directory(r"C:\\Users\\Lenovo\\gitee\\database-project\\our_project\\instance","new_account.csv")
        from flask import send_file 
        download_path = '../instance/inquire_result.csv' 
        response = make_response(send_file(download_path))
        return response


        