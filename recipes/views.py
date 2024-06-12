from django.forms import BaseModelForm
from django.shortcuts import render,HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView ,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from . import models

recipes = [
    {'author':'Hom',
     'title':'gomtha',
     'directions':'combine all ingredients',
     'date_posted':'may 12 2013',
    },
    {'author':'tom',
     'title':'burger',
     'directions':'combine all ingredients',
     'date_posted':'may 12 2013',
    },
    {'author':'nom',
     'title':'gomtha',
     'directions':'combine all ingredients',
     'date_posted':'may 12 2013',
    },
]

# Create your views here.
def home(request):
    recipes = models.Recipe.objects.all()
    context = {
        'recipes':recipes
    }
    return render(request,"recipes/home.html",context)

class RecipeListView(ListView):
    model = models.Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'recipes'

class RecipeDetailView(DetailView):
    model = models.Recipe

class RecipeUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = models.Recipe
    fields = ['title','description']

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class RecipeCreateView(LoginRequiredMixin,CreateView):
    model = models.Recipe
    fields = ['title','description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = models.Recipe
    success_url = reverse_lazy('recipes-home')

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

# from django.contrib.auth.mixins import PermissionRequiredMixin
# from django.views.generic.edit import DeleteView
# from .models import Recipe

# class RecipeDeleteView(PermissionRequiredMixin, DeleteView):
#     model = Recipe
#     permission_required = 'app.delete_recipe'
#     success_url = '/success-url/'  # Redirect after deletion

# from django.contrib.auth.decorators import permission_required
# from django.shortcuts import get_object_or_404, render

# @permission_required('app.delete_recipe', raise_exception=True)
# def delete_recipe_view(request, recipe_id):
#     recipe = get_object_or_404(Recipe, pk=recipe_id)
#     # Delete logic here
#     return render(request, 'recipes/confirm_delete.html', {'object': recipe})


    
def about(request):
    return render(request,"recipes/about.html",{'title':'about us page'})

