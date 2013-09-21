#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Test.
#

import sys
import py
from rpython import conftest
class o:
    view = False
    viewloops = True
#    viewloops = False
conftest.option = o
from rpython.jit.metainterp.test.test_ajit import LLJitMixin

from som.vm.universe import Universe, Exit
import som.compiler.sourcecode_compiler as sourcecode_compiler


cp = py.path.local(__file__).dirpath().dirpath().join("Smalltalk").strpath

class TestLLtype(LLJitMixin):

    def test_inc(self):
        u = Universe()
        u.setup_classpath(cp)
        u._initialize_object_system()
        interp = u.get_interpreter()
        b = u._create_bootstrap_method()
        f = interp.push_new_frame(b)
        src = "C_0 = ( run = ( | tmp | tmp := 1. 1000000 timesRepeat: [ tmp := tmp + 1 ]. ^tmp ))"
        cls = sourcecode_compiler.compile_class_from_string(src, None, u)
        run = cls.lookup_invokable(u.symbol_for("run"))
        
        def interp_w():
            try:
                run.invoke(f, interp)
                interp.start()
            except Exit as e:
                return e.code
            return -1

        self.meta_interp(interp_w, [], listcomp=True, listops=True, backendopt=False)
