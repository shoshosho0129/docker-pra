from django.shortcuts import render, redirect
from django.views import View
from .models import Task
from .forms import TaskForm

# Create your views here.
class IndexView(View):
      def get(self, request):
        no_complete_tasks = list(Task.objects.filter(complete=0).order_by('start_date'))
        complete_tasks = list(Task.objects.filter(complete=1).order_by('start_date'))

        todo_list = no_complete_tasks + complete_tasks

        context = {
            "todo_list": todo_list
        }

        return render(request, "mytodo/index.html", context)
class AddView(View):
    def get(self, request):
        form = TaskForm()
        
        return render(request, "mytodo/add.html", {'form': form})
    
    def post(self, request, *args, **kwargs):
        #登録処理
        #入力データをフォームに渡す
        form = TaskForm(request.POST)
        #入力データに誤りがないかチェック
        is_valid = form.is_valid()
        
        #データが正常であれば
        if is_valid:
            #モデルに登録
            form.save()
            return redirect('/')
        #データが正常じゃない
        return render(request, 'mytodo/add.html',{'form': form})
    
    
class Update_task_complete(View):
    def post(self, request, *args, **kwargs):
        task_id = request.POST.get('task_id')
        
        task = Task.objects.get(id=task_id)
        task.complete = not task.complete
        task.save()
        
        return redirect('/')

class Edit_task(View):
    def get(self, request, task_id):
        task = Task.objects.get(id=task_id)
        form = TaskForm(instance=task)
        return render(request, 'mytodo/edit.html', {'form': form, 'task_id': task_id})
    
    def post(self, request, task_id):
        task = Task.objects.get(id=task_id)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'mytodo/edit.html', {'form': form, 'task_id': task_id})
        
class Delete_task(View):
    def post(self, request, task_id):
        task = Task.objects.get(id=task_id)
        task.delete()
        return redirect('/')
       

# ビュークラスをインスタンス化
index = IndexView.as_view()
add = AddView.as_view()
update_task_complete = Update_task_complete.as_view()
edit = Edit_task.as_view()
delete = Delete_task.as_view()