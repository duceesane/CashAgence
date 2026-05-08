from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import*

def is_admin(user):
    return  user.is_superuser

@login_required
def index(request):
    
    wallets = Wallet.objects.filter(agent=request.user).first()
    txns = Transaction.objects.filter(wallet__agent=request.user)[:3]
    fialed = 'failed'
 
    context = {
        "wallet":wallets,
        "transactions":txns,
        "failed":fialed
    }
    return render(request,"dashboard.html",context)

def topup(request):
    if request.method=="POST":
        tyep_money = request.POST.get("type_money")
        amount = request.POST.get("amount")
        phone = request.POST.get("phone")
        wallet = Wallet.objects.filter(agent=request.user).first()
        transaction = Transaction.objects.create(
            agent=request.user,wallet=wallet,
            phone=phone,amount=int(amount),
            txn_type="deposit",
            type_money=tyep_money,
            status="pending",
            created_at= timezone.now()

        )
        transaction.save()
        
        messages.success(request, f'Top-Up ${amount} oo guulayste wax yar sug ✓')
        return redirect("dashboard")
    
    return render(request,"topup.html")

def payout(request):

    if request.method=="POST":
        
        amount = int(request.POST.get("amount"))
        marchent_id = int(request.POST.get("marchent_id"))
        wallet = Wallet.objects.get(agent=request.user,epos_id=marchent_id)
        if wallet.balance <amount:
            
            messages.error(request, 'Balance kuguma filna')
            return redirect("payout")
        else:
            transaction = Transaction.objects.create(
                agent=request.user,wallet=wallet,
                txn_type="payout",
                amount=amount,
              
                status="success",
                created_at= timezone.now()

            )
            transaction.save()
            wallet.balance -= int(amount)
            wallet.save()
            messages.success(request, f'Lacagta ${amount} la diray ✓')
            return redirect("dashboard")
    wallet = Wallet.objects.filter(agent=request.user)
    context = {
        "wallet":wallet
    }
    return render(request,"payout.html",context)
    
def wallet(request):
    wallets = Wallet.objects.filter(agent=request.user)
    context = {
        "wallets":wallets
    }
    return render(request,"wallet.html",context)

def history(request):
    filter_type = request.GET.get('filter', 'All')
    txns = Transaction.objects.filter(wallet__agent=request.user ).order_by('-created_at')
    failed = "failed"
    if filter_type == 'Deposits':
        txns = txns.filter(txn_type='deposit')
    elif filter_type == 'Payouts':
        txns = txns.filter(txn_type='payout')

    mytags = ['All','Deposits','Payouts']
    wadarta_deposit = Transaction.objects.filter(wallet__agent=request.user,txn_type="deposit")
    wadarta_payout = Transaction.objects.filter(wallet__agent=request.user,txn_type="payout")
    total_payout = 0
    for i in wadarta_payout:
        total_payout += int(i.amount)
    total_deposit = 0
    for total in wadarta_deposit:
        total_deposit += int(total.amount)

    context = {
        "filter_type":filter_type,
        "total_deposit":total_deposit,
        "total_payout":total_payout,
        "mytags":mytags,
        "transactions":txns,
        "failed":failed
    }
    return render(request,"history.html",context)

def profile(request):
    wallets   = Wallet.objects.filter(agent=request.user)
    trns = Transaction.objects.filter(wallet__agent = request.user).count()
    total_comission = sum(w.commission for w in wallets)
    total_wallet = wallets.count()
    context = {
        "wallet":total_wallet,
        "transactions":trns,
        "total_commision":total_comission,
    }

    return render(request,"profile.html",context)

def loginPage(request):
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            messages.success(request,"successifully loged in")
            return redirect('dashboardAdmin' if is_admin(user) else 'dashboard')
        else:
            messages.error(request,"username or password is incorrect")
         
       
    return render(request,"login.html")

def logoutPage(request):

    logout(request)
    return redirect('login')

# ═════════════════════════════════════════════════════════════
# ADMIN — USER MANAGEMENT
# ═════════════════════════════════════════════════════════════
def adminPanel(request):
    codsiyada_pending = Transaction.objects.filter(status = "pending")
    codsiyada_success = Transaction.objects.filter(status = "success").count()
    codsiyada_reject = Transaction.objects.filter(status = "failed").count()
    total_transaction = Transaction.objects.all().count()
    context = {
        "pending":codsiyada_pending,
        "approved":codsiyada_success,
        "reject":codsiyada_reject,
        "total_transaction":total_transaction
    }
    return render(request,"admin/dashboard.html",context)

def create_user(request):
    if request.method =="POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        Username = request.POST.get("Username")
        password = request.POST.get("password")
        is_staff = request.POST.get("is_staff")=="on"
        wallet_name = request.POST.get("wallet_name")
        wallet_logo = request.POST.get("wallet_logo")
        wallet_location = request.POST.get("wallet_location")
        wallet_epos =request.POST.get("wallet_epos")
    
    
        user = User.objects.create_user(first_name=first_name,last_name=last_name,
                            username=Username,password=password,
                            is_staff=is_staff
                            )
        wallet = Wallet.objects.create(agent=user,name=wallet_name,
                    epos_id=wallet_epos,location=wallet_location,
                    logo=wallet_logo,
                    is_active = True
                    )
        user.save()
        wallet.save()
        
        redirect("create-user")
    return render(request,"admin/create_user.html")


def list_user(request):
    users = Wallet.objects.all()
    context = {
        "users":users
    }

    
    return render(request,"admin/users.html",context)

def tapupp_request(request):
    
    status_filter = request.GET.get('status', 'pending')
    requests = Transaction.objects.all()
    if status_filter in ("pending",'success','failed'):

        requests = requests.filter(status=status_filter)
    
    context = {
        "transactions":requests,
        "status_filter":status_filter
    }
    return render(request,"admin/requests.html",context)


def approved(request,pk):
    trn = Transaction.objects.get(id=pk)
    wallet = Wallet.objects.get(epos_id=trn.wallet.epos_id)
    trn.status= "success"
    trn.save()
    wallet.balance += int(trn.amount)
    wallet.save()
    return redirect("dashboardAdmin")

def rejected(request,pk):
    trn = Transaction.objects.get(id=pk)

    trn.status= "failed"
    trn.save()
    return redirect("dashboardAdmin")