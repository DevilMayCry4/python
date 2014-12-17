from django import template

t = template.Template('My name is {{name}}')
c = template.Context({'name':"test"})
print(t.render(c))

