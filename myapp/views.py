from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.db.models import Q
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
import datetime as dt
from django.core.files.storage import default_storage
from dateutil.relativedelta import relativedelta


try:
    l = Login.objects.all()
    to_update = []  
    for z in l:
        d = z.pdate
        if isinstance(d, datetime):  
            d = d.date()

        enddate = d + relativedelta(months=1)

        if enddate <= datetime.now().date():
            z.status = "Pending"
            to_update.append(z)
    if to_update:
        Login.objects.bulk_update(to_update, ["status"])
except:
    pass



def index(request):
    return render(request, "index.html")


def contact(request):
    return render(request, "contact-us.html")


def User_reg(request):
    current_date = datetime.today().strftime("%Y-%m-%d")
    print(current_date)
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        password = request.POST["password"]
        title = request.POST["title"]
        image = request.FILES["image"]
        print(email)
        if Login.objects.filter(username=email).exists():
            messages.error(request, "User already exists")
        else:
            logUser = Login.objects.create_user(
                username=email,
                password=password,
                userType="User",
                viewPass=password,
                is_active=1,
            )
            logUser.save()

            userReg = UserRegistration.objects.create(
                name=name,
                title=title,
                email=email,
                phone=phone,
                address=address,
                loginid=logUser,
                image=image,
            )
            userReg.save()
            messages.error(request, "Successfully created")

    return render(request, "Registration.html", {"current_date": current_date})


def client_reg(request):
    current_date = datetime.today().strftime("%Y-%m-%d")
    print(current_date)
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        password = request.POST["password"]
        image = request.FILES["image"]
        proof = request.FILES["proof"]
        if Login.objects.filter(username=email).exists():
            messages.error(request, "User already exists")
        else:
            logUser = Login.objects.create_user(
                username=email,
                password=password,
                userType="Client",
                viewPass=password,
                is_active=0,
            )
            logUser.save()

            userReg = Client_reg.objects.create(
                name=name,
                email=email,
                phone=phone,
                address=address,
                loginid=logUser,
                image=image,
                proof=proof
            )
            userReg.save()
            messages.error(request, "Successfully created")

    return render(request, "Company_reg.html")


def logins(request):
    if request.POST:
        email = request.POST["email"]
        passw = request.POST["password"]
        user = authenticate(username=email, password=passw)
        print(user)

        if user is not None:
            login(request, user)

            if  user.is_active:
                if user.is_superuser:
                    messages.info(request, "Login Success")
                    return redirect("/admhome")
                elif user.userType == "Admin":
                    messages.info(request, "Login Success")
                    return redirect("/admhome")
                elif user.userType == "User":
                    id = user.id
                    email = user.username
                    userType = user.userType
                    request.session["uid"] = id
                    request.session["type"] = userType
                    request.session["email"] = email
                    messages.info(request, "Login Success")
                    return redirect("/userhome")
                elif user.userType == "Client":
                    id = user.id
                    email = user.username
                    request.session["cid"] = id
                    userType = user.userType
                    request.session["type"] = userType
                    request.session["email"] = email
                    if user.status == "Pending":
                        return redirect(f"/upayment?id={id}")
                    else:
                        messages.info(request, "Login Success")
                        return redirect("/clienthome")
                else:
                    messages.info(request, "type Not Defined")
            else:
                messages.error(request, "User is not Approved by Admin")
        else:
            print("Hiii")
            messages.error(request, "Invalid Username/Password")
    return render(request, "login.html")


def admhome(request):
    return render(request, "Admin/index.html")


def clienthome(request):
    posts=Posts.objects.all().order_by('-id')
    uid = request.session["cid"]
    view = Client_reg.objects.get(loginid=uid)
    if request.POST:
        user = request.POST['userid']
        salary=request.POST['salary']
        desc=request.POST['message']
        user = UserRegistration.objects.get(id=user)
        req=Requests.objects.create(user=user,company=view,salary=salary,message=desc)
        req.save()
        messages.info(request, "Request Sent Successfully")
    return render(request, "Client/index.html",{"posts":posts})


def userhome(request):
    return render(request, "User/index.html")


def admviewusers(request):
    view = UserRegistration.objects.all()
    return render(request, "Admin/view_users.html", {"view": view})


def admviewclient(request):
    view = Client_reg.objects.all()
    return render(request, "Admin/view_company.html", {"view": view})


def change(request):
    Job_Application.objects.filter(id=1).delete()

    return HttpResponse("Changed")


def approve_client(request):
    mid = request.GET.get("cid")
    app = Login.objects.filter(id=mid).update(is_active=1)
    if app == True and request.GET['utype'] == 'Client':
        messages.info(request, "Client Approved Successfully")
        return redirect("/admviewclient")
    elif app == True and request.GET['utype'] == 'User':
        messages.info(request, "User Approved Successfully")
        return redirect("/admviewusers")


def reject_client(request):
    mid = request.GET.get("cid")
    app = Login.objects.filter(id=mid).update(is_active=0)
    if app == True and request.GET['utype'] == 'Client':
        messages.info(request, "Client Rejected Successfully")
        return redirect("/admviewclient")
    elif app == True and request.GET['utype'] == 'User':
        messages.info(request, "User Rejected Successfully")
        return redirect("/admviewusers")


def add_job(request):
    cid = request.session["cid"]
    client_id = Client_reg.objects.get(loginid=cid)
    print(client_id)
    current_date = datetime.today().strftime("%Y-%m-%d")
    if request.POST:
        j_title = request.POST["name"]
        salary = request.POST["salary"]
        job_type = request.POST["job_type"]
        ex_level = request.POST["ex_level"]
        # address = request.POST["address"]
        Description = request.POST["Description"]
        image = request.FILES["image"]
        if request.POST:
            add = Job_Portal.objects.create(
                cid=client_id,
                jname=j_title,
                job_type=job_type,
                salary=salary,
                ex_level=ex_level,
                description=Description,
                image=image,
                date=current_date,
            )
            add.save()
    return render(request, "Client/add_vacancy.html")


def client_job_view(request):
    cid = request.session["cid"]
    view = Job_Portal.objects.filter(cid_id__loginid=cid)
    print(view)
    return render(request, "Client/view_job.html", {"view": view})


def delete_job(request):
    jid = request.GET.get("id")
    app = Job_Portal.objects.filter(id=jid).delete()
    messages.info(request, "Job Deleted Successfully")
    return redirect("/client_job_view")


def search_jobs(request):
    return render(request, "User/job-search.html")


def view_jobs(request):
    view = Job_Portal.objects.all()
    return render(request, "User/job-category.html", {"view": view})


def apply_job(request):
    jid = request.GET.get("jid")
    uid = request.session["uid"]
    # print(uid)
    cid = request.GET.get("cid")
    jjid = Job_Portal.objects.get(id=jid)
    client_id = Client_reg.objects.get(id=cid)
    Uidd = UserRegistration.objects.get(loginid__id=uid)
    print(Uidd)
    print(client_id)
    current_date = datetime.today().strftime("%Y-%m-%d")
    if request.POST:
        if Uidd.loginid.status == "Pending":
                return redirect(f"/upayment?id={Uidd.loginid.id}")
        else:
                education = request.POST["Highest"]
                Field = request.POST["Field"]
                cv = request.FILES["cv"]
                if Job_Application.objects.filter(
                    user=Uidd, job=jjid, company=client_id
                ).exists():
                    messages.error(request, "You Are already Applied For This Position")
                else:
                    insert = Job_Application.objects.create(
                        company=client_id,
                        user=Uidd,
                        job=jjid,
                        date=current_date,
                        education=education,
                        field=Field,
                        resume=cv,
                    )
                    insert.save()

                return redirect("/job_applied")

    return render(request, "User/apply_job.html")


def job_applied(request):
    return render(request, "User/Applied_success.html")


def userview_job_applied(request):
    uid = request.session["uid"]
    print(uid)
    view = Job_Application.objects.filter(user__loginid=uid)
    count = Job_Application.objects.filter(user__loginid=uid).count()

    print("total count", count)
    # view=Job_Application.objects.filter(user__loginid=uid)
    # view=Job_Application.objects.filter(user__loginid=uid)
    return render(request, "User/applied_job.html", {"view": view, "count": count})


def client_view_applications(request):
    cid = request.session["cid"]
    view = Job_Application.objects.filter(company__loginid=cid, status="Applied")
    view2 = Job_Application.objects.filter(company__loginid=cid, status="Approved")
    if request.POST:
        req = request.POST['rid']
        r=Job_Application.objects.get(id=req)
        r.interviewdate=request.POST['interviewdate']
        r.interviewtime=request.POST['interviewtime']
        r.save()
        messages.info(request, "Interview Scheduled Successfully")
    return render(
        request, "Client/view_application.html", {"view": view, "view2": view2}
    )


def approve_ap(request):
    aid = request.GET.get("id")
    app = Job_Application.objects.filter(id=aid, status="Applied").update(
        status="Approved"
    )
    if app == True:
        messages.info(request, "Client Approved Successfully")
    return redirect("/view_applications")


def reject_ap(request):
    aid = request.GET.get("aid")
    app = Job_Application.objects.filter(id=aid, status="Applied").update(
        status="Rejected"
    )
    if app == True:
        messages.info(request, "Client Rejected Successfully")
    return redirect("/view_applications")


def add_work(request):
    jid = request.GET.get("jid")
    cid = request.session["cid"]
    uid = request.GET.get("id")
    jjid = Job_Portal.objects.get(id=jid)
    client_id = Client_reg.objects.get(loginid=cid)
    Uidd = UserRegistration.objects.get(id=uid)
    print(client_id)
    current_date = datetime.today().strftime("%Y-%m-%d")
    if request.POST:
        title = request.POST["name"]
        # pdate=request.POST["pdate"]
        ldate = request.POST["ldate"]
        desc = request.POST["desc"]
        cv = request.FILES["work_file"]
        # if Work.objects.filter(user=Uidd).exists():
        #     messages.error(request, "You Are already Applied For This Position")
        # else:
        insert = Work.objects.create(
            job=jjid,
            title=title,
            pdate=current_date,
            ldate=ldate,
            company=client_id,
            user=Uidd,
            desc=desc,
        )
        insert.save()

        messages.info(request, "Work Added Successfully")

    return render(request, "Client/add_work.html")


def client_view_staffs(request):
    cid = request.session["cid"]
    client_id = Client_reg.objects.get(loginid=cid)
    view = Job_Application.objects.filter(company=client_id, status="Approved")
    return render(request, "Client/view_staffs.html", {"view": view})


def userchat(request):
    cid = request.GET.get("cid")
    remail = request.GET.get("email")
    client_id = Client_reg.objects.get(id=cid)
    uid = request.session["uid"]
    print(uid)
    Uidd = UserRegistration.objects.get(loginid=uid)
    print("id", Uidd)
    semail = request.session["email"]
    type = request.session["type"]

    time = datetime.now().time()
    date = datetime.now().date()
    formatted_time = time.strftime("%I:%M %p")
    formatted_date = date.strftime("%B %d")

    chats = Message.objects.filter(Q(senderemail=semail) | Q(reciveremail=semail))

    if request.POST:
        message = request.POST["message"]

        sendMsg = Message.objects.create(
            message=message,
            date=formatted_date,
            time=formatted_time,
            type="Freelacer",
            sender=client_id,
            receiver=Uidd,
            senderemail=semail,
            reciveremail=remail,
        )
        sendMsg.save()
    return render(request, "User/chat.html", {"chats": chats})


def clientchat(request):
    uid = request.GET.get("id")
    remail = request.GET.get("email")
    uid_id = UserRegistration.objects.get(id=uid)
    semail = request.session["email"]
    cid = request.session["cid"]
    client_id = Client_reg.objects.get(loginid=cid)

    type = "Client"
    time = datetime.now().time()
    date = datetime.now().date()
    formatted_time = time.strftime("%I:%M %p")
    formatted_date = date.strftime("%B %d")

    chats = Message.objects.filter(Q(senderemail=semail) | Q(reciveremail=semail))

    print("Chats", chats)
    print(uid)

    if request.POST:
        message = request.POST["message"]
        sendMsg = Message.objects.create(
            message=message,
            date=formatted_date,
            time=formatted_time,
            type="Client",
            sender=client_id,
            receiver=uid_id,
            senderemail=semail,
            reciveremail=remail,
        )
        sendMsg.save()
        # elif type == "Admin":
        #     sendMsg = Message.objects.create(
        #         message=message,
        #         date=formatted_date,
        #         time=formatted_time,
        #         type="Admin",
        #         sender=aid,
        #         receiver=childid,
        #     )
        #     sendMsg.save()
    return render(request, "Client/chat.html", {"chats": chats})


def freelacer_view_work(request):
    # wid=request.GET["id"]

    if request.GET:
        wid = request.GET["id"]
        status = request.GET["status"]
        upda = Work.objects.filter(id=wid).update(status=status)

    uid = request.session["uid"]
    view = Work.objects.filter(user__loginid=uid)

    return render(request, "User/view_work_file.html", {"view": view})


def total_works(request):
    cid = request.session["cid"]

    view = Work.objects.filter(company__loginid=cid)
    return render(request, "Client/total_works.html", {"view": view})


from itertools import chain


def search_users(request):
    cid = request.session["cid"]
    # feed=Feedback.objects.all()
    # view=UserRegistration.objects.all()
    feedback_query = Feedback.objects.all()
    user_registration_query = UserRegistration.objects.all()
    merged_query = zip(user_registration_query, feedback_query)
    merged_list = list(merged_query)
    print(merged_list)
    return render(
        request, "Client/search_users.html", {"view": user_registration_query}
    )


# def search_chats(request):
#     uid=request.GET.get("id")
#     remail=request.GET.get("email")
#     uid_id=UserRegistration.objects.get(id=uid)
#     print(uid_id)
#     semail = request.session["email"]
#     cid = request.session["cid"]
#     client_id=Client_reg.objects.get(loginid=cid)

#     type = "Client"
#     time = datetime.now().time()
#     date = datetime.now().date()
#     formatted_time = time.strftime("%I:%M %p")
#     formatted_date = date.strftime("%B %d")


#     chats = Message.objects.filter(Q(senderemail=semail) | Q(reciveremail=semail))

#     print("Chats", chats)
#     print(uid)

#     if request.POST:
#         message = request.POST["message"]
#         sendMsg = Message.objects.create(
#                 message=message,
#                 date=formatted_date,
#                 time=formatted_time,
#                 type="Client",
#                 sender=client_id,
#                 receiver=uid_id,
#                 senderemail=semail,
#                 reciveremail=remail
#             )
#         sendMsg.save()
#         # elif type == "Admin":
#         #     sendMsg = Message.objects.create(
#         #         message=message,
#         #         date=formatted_date,
#         #         time=formatted_time,
#         #         type="Admin",
#         #         sender=aid,
#         #         receiver=childid,
#         #     )
#         #     sendMsg.save()
#     return render(request, "Client/search_chat.html",{"chats":chats})


def payment_page(request):
    wid = request.GET.get("wid")

    if request.POST:
        update = Work.objects.filter(id=wid).update(payment="Paid")
        return redirect("/total_works")

    return render(request, "Client/payment_page.html")


def amount_page(request):
    wid = request.GET.get("wid")
    uid = request.GET.get("uid")
    uid_id = UserRegistration.objects.get(id=uid)
    wid_id = Work.objects.get(id=wid)
    print("that id : ", wid_id)

    if request.POST:
        amount = request.POST["amount"]

        update = Work.objects.filter(id=wid, user=uid_id).update(amount=amount)
        return redirect("/payment_page?wid=" + wid)
        # if update  == True:

    return render(request, "Client/amount.html")


def add_feed(request):
    wid = request.GET.get("wid")
    uid = request.GET.get("uid")
    uid_id = UserRegistration.objects.get(id=uid)
    wid_id = Work.objects.get(id=wid)
    cid = request.session["cid"]
    cid_id = Client_reg.objects.get(loginid_id=cid)

    feedData = Feedback.objects.filter(Q(cid__loginid=cid) & Q(uid=uid)).values_list(
        "rating", flat=True
    )
    count = Feedback.objects.filter(Q(cid__loginid=cid) & Q(uid=uid)).count()
    summavg = sum(feedData)

    if request.POST:
        feed = request.POST["feed"]
        rating = request.POST["rating"]
        # avg+=rating
        totalRating = int(summavg) + int(rating)
        avg = totalRating / (count + 1)
        print(avg)

        if Feedback.objects.filter(wid=wid_id, cid=cid_id).exists():
            messages.info(request, "Already Rated")

        else:
            send = Feedback.objects.create(
                cid=cid_id, feed=feed, rating=rating, wid=wid_id, uid=uid_id, Tavg=avg
            )
            send.save()
            up = UserRegistration.objects.filter(loginid__id=uid).update(Rating=avg)
            print("id", up)
            messages.info(request, "Rating Added Successfully")

    return render(request, "Client/feedback.html")


def calculate_average_rating(ratings, request):
    uid = request.session["uid"]
    items = Feedback.objects.filter(uid=uid)
    ratings = Feedback.objects.filter(uid=uid).values_list("rating", flat=True)
    total_ratings = len(ratings)
    if total_ratings == 0:
        return 0  # Handle the case when there are no ratings

    total_sum = sum(ratings)
    average_rating = total_sum / total_ratings

    return average_rating


# # Call the function with the "ratings" list
# average_rating = calculate_average_rating(ratings)
# print(f"The average rating is: {average_rating:.2f}")


def user_payment_details(request):
    wid = request.GET.get("wid")
    uid = request.session["uid"]
    view = Work.objects.filter(user__loginid=uid)
    return render(request, "User/payment_details.html", {"view": view})


def user_profile(request):
    uid = request.session["uid"]
    view = UserRegistration.objects.filter(loginid__id=uid)

    return render(request, "User/profile.html", {"view": view})


def update_profile(request):
    id = request.GET.get("id")
    email = request.GET.get("email")
    get = UserRegistration.objects.filter(id=id)
    print(get)
    current_date = datetime.today().strftime("%Y-%m-%d")
    print(current_date)

    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        password = request.POST["password"]
        title = request.POST["title"]
        image = request.FILES["image"]
        resume = request.FILES["resume"]

        if image or resume:

            userReg = UserRegistration.objects.filter(id=id).update(
                name=name,
                title=title,
                email=email,
                phone=phone,
                address=address,
            )
            update_resume = UserRegistration.objects.get(id=id)
            update_resume.resume = resume
            update_resume.save()

            update = UserRegistration.objects.get(id=id)
            update.image = image
            update.save()

            logUser = Login.objects.filter(username=email).update(
                username=email,
                viewPass=password,
            )
            logUpdate = Login.objects.get(username=email)
            logUpdate.set_password(password)
            logUpdate.save()
            messages.error(request, "Profile Updated")

        else:
            userReg = UserRegistration.objects.filter(id=id).update(
                name=name,
                title=title,
                email=email,
                phone=phone,
                address=address,
            )
            logUser = Login.objects.filter(username=email).update(
                username=email,
                viewPass=password,
            )
            logUpdate = Login.objects.get(username=email)
            logUpdate.set_password(password)
            logUpdate.save()
            messages.error(request, "Profile Updated")

    return render(request, "User/update_profile.html", {"view": get})


def delete_ap(request):
    id = request.GET.get("id")
    Dele = Job_Application.objects.filter(id=id).delete()
    return HttpResponse(
        "<script>alert('Delete Profile');window.location='/view_applications'</script>"
    )


def udp(request):
    up = Login.objects.filter(id=4).delete()
    return HttpResponse("deleted")


def add_guidence(request):
    if request.method == "POST":
        name = request.POST.get("name")
        url = request.POST.get("url")
        desc = request.POST.get("desc")

        ins = Guidence.objects.create(name=name, url=url, desc=desc)
        ins.save()
        return HttpResponse(
            "<script>alert('Guidence Added');window.location='/add_guidence';</script>"
        )

    return render(request, "Admin/add_guidence.html")


def user_view_guide(request):
    user=UserRegistration.objects.get(loginid__id=request.session["uid"])
    view = Guidence.objects.all()
    chats=UserAdminChat.objects.filter(user = user )
    if request.POST:
        message = request.POST["message"]
        sendMsg = UserAdminChat.objects.create(
            usermessage=message,
            user=user,
        )
        sendMsg.save()

    return render(request, "User/view_guide.html", {"view": view,"chats":chats})


def company_profile(request):
    uid = request.session["cid"]
    view = Client_reg.objects.filter(loginid=uid)
    return render(request, "Client/profile.html", {"view": view})


def company_update_profile(request):
    uid=request.session["cid"]
    email = request.GET.get("email")
    get = Client_reg.objects.filter(loginid=uid,email=email)
    print(get)
    current_date = datetime.today().strftime("%Y-%m-%d")
    print(current_date)

    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        password = request.POST["password"]
        image = request.FILES.get("image")

        if image :

            userReg = Client_reg.objects.filter(loginid=uid).update(
                name=name,
                email=email,
                phone=phone,
                address=address,
            )
            update = Client_reg.objects.get(loginid=uid)
            update.image = image
            update.save()

            logUser = Login.objects.filter(id=uid,username=email).update(
                username=email,
                viewPass=password,
            )
            logUpdate = Login.objects.get(id=uid,username=email)
            logUpdate.set_password(password)
            logUpdate.save()
            messages.error(request, "Profile Updated")

        else:
            userReg = Client_reg.objects.filter(id=uid,email=email).update(
                name=name,
                email=email,
                phone=phone,
                address=address,
            )
            logUser = Login.objects.filter(username=email).update(
                username=email,
                viewPass=password,
            )
            logUpdate = Login.objects.get(username=email)
            logUpdate.set_password(password)
            logUpdate.save()
            messages.error(request, "Profile Updated")

    return render(request, "Client/update_profile.html", {"view": get})

def userfeedbacks(request):
    uid = request.session["uid"]

    cid=request.GET.get("wid")
    view = UserFeedback.objects.filter(wid=cid)
    return render(request, "User/userfeedbacks.html", {"feedbacks": view})

def useraddfeedback(request):
    wid = request.GET.get("wid")
    uid = request.session["uid"]
    uid_id = UserRegistration.objects.get(loginid__id=uid)
    wid_id = Job_Portal.objects.get(id=wid)
    print("that id : ", wid_id)
    feedbacks = UserFeedback.objects.filter(Q(wid=wid_id) & Q(uid=uid_id))
    if request.POST:
        feed = request.POST["feed"]
        

        send = UserFeedback.objects.create(
         feed=feed, wid=wid_id, uid=uid_id
        )
        send.save()

        messages.info(request, "Rating Added Successfully")

    return render(request, "User/useraddfeedback.html",{"feedbacks":feedbacks})

def delete_feedback(request):
    id = request.GET.get("id")
    Dele = UserFeedback.objects.get(id=id)
    wid = Dele.wid_id
    Dele.delete()
    
    return HttpResponse(
        "<script>alert('Delete Feedback');window.location='/useraddfeedback?wid="+ str(wid) +"'</script>"
    )

def view_feedbacks(request):
    id=request.GET.get("id")
    view = UserFeedback.objects.filter(wid__cid__id=id)
    return render(request, "Admin/view_feedbacks.html", {"feedbacks": view})

def newimages(request):
    user = UserRegistration.objects.get(loginid__id=request.session["uid"])
    posts=Posts.objects.filter(user=user)
    msg=""
    if request.method == "POST":
        image = request.FILES.get("image")
        title = request.POST.get("title")
        description = request.POST.get("description")
        post = Posts.objects.create(user=user, image=image, desc=description,title=title)
        post.save()
        msg="Image Uploaded Successfully"

    return render(request, "User/newpost.html",{"posts":posts,"msg":msg})

def delete_post(request):
    id = request.GET.get("id")
    Dele = Posts.objects.filter(id=id)
    Dele.delete()
    return HttpResponse(
        "<script>alert('Delete Post');window.location='/newimages'</script>"
    )

def requestuser(request):
    user=UserRegistration.objects.get(loginid__id=request.session["uid"])
    requests= Requests.objects.filter(user=user)
    return render(request, "User/requestuser.html",{ "requests":requests})

def togglerequestuser(request):
    id = request.GET.get("id")
    status = request.GET.get("status")
    upda = Requests.objects.get(id=id)
    upda.status=status
    upda.save()
    return redirect("/requestuser")

def requestscompany(request):
    user=Client_reg.objects.get(loginid__id=request.session["cid"])
    requests= Requests.objects.filter(company=user).order_by('-id')
    if request.POST:
        req = request.POST['rid']
        r=Requests.objects.get(id=req)
        r.status="Interview Scheduled"
        r.interviewdate=request.POST['interviewdate']
        r.interviewtime=request.POST['interviewtime']
        r.save()
        messages.info(request, "Interview Scheduled Successfully")
    return render(request, "Client/requestscompany.html",{ "requests":requests})


def adminhelp(request):
    user=UserRegistration.objects.get(id=request.GET['id'])
    chats=UserAdminChat.objects.filter(user = user )
    if request.POST:
        message = request.POST["message"]
        sendMsg = UserAdminChat.objects.create(
            adminmessage=message,
            user=user,
        )
        sendMsg.save()
        return redirect("/adminhelp?id="+str(user.id))
    return render(request, "Admin/adminhelp.html",{"chats":chats})

def adminpayment(request):
    n=UserPayment.objects.all().count()
    userpayment=Allpayments.objects.all()
    if n==0:
        amounts=None
    else:
        n-=1
        amounts=UserPayment.objects.all()[n]
    
    if request.POST:
        user_amount = request.POST["useramount"]
        client_amount = request.POST["clientamount"]
        send = UserPayment.objects.create(
         user_amount=user_amount, client_amount=client_amount
        )
        send.save()
        messages.info(request, "Payment Added Successfully")
    return render(request, "Admin/adminpayment.html",{"amounts":amounts,"userpayment":userpayment})

def upayment(request):
    id=request.GET.get("id")
    login = Login.objects.get(id=id)
    view = UserPayment.objects.all().order_by('-id')[0]
    if login.userType=="User":
        amount=view.user_amount
    else:
        amount=view.client_amount
    if request.POST:
        login.pdate = datetime.now()
        login.status = "Paid"
        login.save()
        messages.info(request, "Payment Added Successfully")
        pay=Allpayments.objects.create(amount=amount,user=login)
        pay.save()
        if login.userType == "User":
            return redirect("/view_jobs")
        else:
            return redirect("/login")

    return render(request, "upayment.html",{"view":view,"amount":amount})