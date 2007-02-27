from zope.component import getMultiAdapter, getUtility
from zope.publisher.interfaces.browser import IBrowserPublisher

from Acquisition import aq_base, aq_parent, Explicit

from plone.contentrules.engine.interfaces import IRuleStorage

from plone.app.contentrules.rule import Rule
from plone.app.contentrules.tests.base import ContentRulesTestCase

from dummy import DummyCondition, DummyAction

class TestTraversal(ContentRulesTestCase):

    def afterSetUp(self):
        self.setRoles(('Manager',))

    def testTraverseToRule(self):
        r = Rule()
        storage = getUtility(IRuleStorage)
        storage[u'r1'] = r
        traversed = self.portal.restrictedTraverse('++rule++r1')
        self.failUnless(aq_parent(traversed) is self.portal)
        self.failUnless(aq_base(traversed) is r)
    
    def testTraverseToRuleCondition(self): 
        r = Rule()
        e1 = DummyCondition()
        e2 = DummyCondition()
        r.conditions.append(e1)
        r.conditions.append(e2)
        storage = getUtility(IRuleStorage)
        storage[u'r1'] = r
        
        tr = self.portal.restrictedTraverse('++rule++r1')
        te1 = tr.restrictedTraverse('++condition++0')
        te2 = tr.restrictedTraverse('++condition++1')
        
        self.failUnless(aq_parent(te1) is tr)
        self.failUnless(aq_base(te1) is e1)
        
        self.failUnless(aq_parent(te2) is tr)
        self.failUnless(aq_base(te2) is e2)
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTraversal))
    return suite