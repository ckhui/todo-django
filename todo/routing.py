from channels.routing import ProtocolTypeRouter, URLRouter
import task.routing

application = ProtocolTypeRouter({
    'http': URLRouter(task.routing.urlpatterns),
})