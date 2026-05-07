from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="dashboard"),
    path("topup/",views.topup,name="topup"),
    path("payout/",views.payout,name="payout"),
    path("wallet/",views.wallet,name="wallet"),
    path("history/",views.history,name="history"),
    path("profile/",views.profile,name="profile"),
    path("login/",views.loginPage,name="login"),
    path("logout/",views.logoutPage,name="logout"),
    
    # ── Admin Pages ───────────────────────────────────────────
    path("admin-panel/",views.adminPanel,name="dashboardAdmin"),
    path("create-user/",views.create_user,name="create-user"),
    path("list-user/",views.list_user,name="list-user"),
    path("approved/<int:pk>",views.approved,name="approved"),
    path("rejected/<int:pk>",views.rejected,name="rejected"),
   
    path("codsiyada/",views.tapupp_request,name="codsiyada")

]
