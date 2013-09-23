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


    def _compile(self, source, start):
        u = Universe()
        u.setup_classpath(cp)
        u._initialize_object_system()
        interp = u.get_interpreter()
        b = u._create_bootstrap_method()
        frame = interp.push_new_frame(b)
        cls = sourcecode_compiler.compile_class_from_string(source, None, u)
        obj = u.new_instance(cls)
        frame.push(obj)
        invokable = cls.lookup_invokable(u.symbol_for(start))
        return (u, frame, invokable)

    def test_inc(self):
        universe, frame, invokable = self._compile(
            """
            C_0 = (
                run = ( | tmp |
                        tmp := 1.
                        10000 timesRepeat: [
                          tmp := tmp + 1 ].
                        ^tmp
                )
            )
            """, "run")
        def interp_w():
            try:
                universe.start(frame, invokable)
            except Exit as e:
                return e.code
            return -1

        self.meta_interp(interp_w, [],
                         listcomp=True, listops=True, backendopt=True)

    def test_rec(self):
        universe, frame, invokable = self._compile(
            """
            C_1 = (
                count: n = ( ^ (n > 0)
                                 ifTrue: [self count: n - 1]
                                 ifFalse: [n]
                )
                run = ( ^ self count: 100000 )
            )
            """, "run")
        def interp_w():
            try:
                universe.start(frame, invokable)
            except Exit as e:
                return e.code
            return -1

        self.meta_interp(interp_w, [],
                         listcomp=True, listops=True, backendopt=True)
