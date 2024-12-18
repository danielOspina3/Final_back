from request.view import CustomUserManagerView, view_support,view_Ips,view_comments
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from request.view.view_auth import  UserList, UserDetail, CustomAuthToken, CreateUserAPIView, LoginView, CustomTokenObtainPairView
from .view import CustomUserManagerView,view_auth,view_comments,view_Ips,view_support,view_type_of_request,view_Subtype_of_request,viewMySupport


urlpatterns = [
    
    
    path('login', LoginView.as_view(), name='token_obtain_pair'),
    
    #* Users
    path('view-user', CustomUserManagerView.getUser, name='view_user' ),#sirve
    path('view-users', CustomUserManagerView.getUsers, name='view_users' ),#sirve
    
    
    #* Ips
    path('view-ips', view_Ips.getEPS, name='view-ips' ),
    path('view-ips-active', view_Ips.getEPSActive, name='view-ips-active' ),
    path('create-ips', view_Ips.createEPS, name='create-ips' ),
    path('update-ips/<int:pk>', view_Ips.updateIpsActive, name='update-ips' ),
    path('ips-list-one/<int:pk>', view_Ips.getOneIps ),
    path('municipio-list', view_Ips.getMunicipio),
    
    
    #* comments
    path('view-comment', view_comments.getComments, name='view-comment' ),
    path('create-comment', view_comments.createComments, name='create-comment' ),
    path('update-comment', view_comments.updateComment, name='update-comment' ),
    
    
    
    #* support
    path('create-support', view_support.createSupport, name='create-support' ),#sirve
    path('view-support', view_support.supportGetAll, name='view-support' ),#sirve
    path('view-support-final', view_support.supportGetAllFinal, name='view-support-final' ),#sirve
    path('update-support', view_support.updateSupport, name='update-support' ),
    path('support-list-one/<int:pk>', view_support.getOneSupport),#sirve
    path('update-supportUser2/<int:pk>', view_support.update_customeruser2),#sirve}
    path('update-supporDetails/<int:pk>', view_support.update_support_details),  # Cambiado para usar el nuevo método

    
    # * user routes, using views and auth
    path('users', UserList.as_view(), name='user-list'),
    path('users/<int:pk>', UserDetail.as_view(), name='user-list-id'),
    path('create-user', CreateUserAPIView.as_view(), name='api-create-user'),
    path('login', LoginView.as_view(), name='token_obtain_pair'),
    path('token', CustomTokenObtainPairView.as_view(), name='token'),
    path('user-status-update/<int:pk>', CustomUserManagerView.updateUserIsActive),
    path('update-user/<int:pk>', CustomUserManagerView.updateUser),

    path('user-list', CustomUserManagerView.getUser),
    path('user-list-one/<int:pk>', CustomUserManagerView.getOneUser),
    path('user-list-one-rol/<int:pk>', CustomUserManagerView.getOneUserRol),
    
    path('Subtype-create', view_Subtype_of_request.createSubType_of_request),
    path('Subtype-list-one/<int:pk>', view_Subtype_of_request.getOneSubType),
    path('Subtype-list', view_Subtype_of_request.getSubType_of_request),
    # urls.py
    path('Subtype-list-type/<int:number>/', view_Subtype_of_request.getSubType_of_request_type),

    
   
    path('type-of-request-list', view_type_of_request.getType_request),
    path('create-type-of-request', view_type_of_request.createType_of_request),
    path('view-mysupport/<int:id>', viewMySupport.getbysupport),
    path('support-export', view_support.export_supports_to_excel),
   
    
    
    
]
urlpatterns = format_suffix_patterns(urlpatterns)
