from unittest import TestCase

from git_diff_lines.parser import parse

diff_output = '''
diff --git a/.pylintrc b/.pylintrc
new file mode 100644
index 0000000..c4a9d6d
--- /dev/null
+++ b/.pylintrc
@@ -0,0 +1,10 @@
+[BASIC]
+good-names=_,a,b,c,d,e,ex,i,j,k,n,p,rv,t,v,db
+
+[MASTER]
+disable=
+    C0114, # missing-module-docstring
+    C0116, # Missing function or method docstring
+    R0903, # Too few public methods
+    R0201, # Method could be a function
+    C0115, # Missing class docstring
\ No newline at end of file
diff --git a/simple/models.py b/simple/models.py
index 30e2ebb..a0c837e 100644
--- a/simple/models.py
+++ b/simple/models.py
@@ -1,7 +1,6 @@
-from django.db import models
+from django.db import models # changed
 
-
-def div(a, b): ##
-    if b == 0: ##
-        return 0 ## 
-    return a / b ##
+def div(a, b): #
+    if b == 0 or False: #
+        return 0 #
+    return a / b #
'''

class TestParser(TestCase):
    
    def test_empty_input(self):
        self.assertEqual(set(), parse(''))
        self.assertEqual(set(), parse('     \n      \n    \n\n\n\n'))

    def test_real_world_example(self):
        expected = {
            ('.pylintrc', 1),
            ('.pylintrc', 2),
            ('.pylintrc', 3), 
            ('.pylintrc', 4), 
            ('.pylintrc', 5), 
            ('.pylintrc', 6),
            ('.pylintrc', 8),
            ('.pylintrc', 7),
            ('.pylintrc', 9),
            ('.pylintrc', 10), 

            ('simple/models.py', 1),
            ('simple/models.py', 2),
            ('simple/models.py', 3),
            ('simple/models.py', 4),
            ('simple/models.py', 5), 
            ('simple/models.py', 6), 
            ('simple/models.py', 7), 
        }
        self.assertEqual(expected, parse(diff_output))

    def test_a_range_is_not_valid(self):
        faulty_diff_lines = diff_output.replace('+1,10', '0')
        res = parse(faulty_diff_lines)
        self.assertNotIn(('.pylintrc', 3), res)

    def test_invalid_input(self):
        for invalid_input in [1, set, 1.1, [], None, 'adsfads', 'asdf\nadsf']:
            self.assertEqual(set(), parse(invalid_input))
