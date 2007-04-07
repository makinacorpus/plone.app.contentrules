from OFS.SimpleItem import SimpleItem
from zope.component import adapts, queryUtility, getUtility
from zope.component.interfaces import ComponentLookupError
from zope.interface import Interface, implements
from zope.formlib import form
from zope import schema

from plone.app.contentrules.browser.formhelper import AddForm, EditForm 
from plone.contentrules.rule.interfaces import IRuleElementData, IExecutable

from Products.CMFCore.interfaces import IURLTool
from Products.CMFPlone import PloneMessageFactory as _
from Products.MailHost.interfaces import IMailHost


class IMailAction(Interface):
    """Definition of the configuration available for a mail action
    """
    subject = schema.TextLine(title=_(u"Subject"),
                              description=_(u"Subject of the message"),
                              required=True)
    source = schema.TextLine(title=_(u"Email source"),
                             description=_("The email address that sends the \
email. If no email is provided here, it will use the portal from address."),
                             required=False)
    recipients = schema.TextLine(title=_(u"Email recipients"),
                                description=_("The email where you want to \
send this message. To send it to different email addresses, just separate them\
 with ,"),
                                required=True)
    message = schema.Text(title=_(u"Message"),
                          description=_(u"Type in here the message that you \
want to mail. Some defined content can be replaced: ${title} will be replaced \
by the title of the newly created item. ${url} will be replaced by the \
URL of the newly created item"),
                          required=True)

class MailAction(SimpleItem):
    """
    The implementation of the action defined before
    """
    implements(IMailAction, IRuleElementData)

    subject = ''
    source = ''
    recipients = ''
    message = ''

    element = 'plone.actions.Mail'

    @property
    def summary(self):
        return _(u"Email report to ${recipients}",
                 mapping=dict(recipients=self.recipients))


class MailActionExecutor(object):
    """The executor for this action.
    """
    implements(IExecutable)
    adapts(Interface, IMailAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        recipients = [str(mail.strip()) for mail in \
                      self.element.recipients.split(',')]
        mailhost = queryUtility(IMailHost)
        if not mailhost:
            raise ComponentLookupError, 'You must have a Mailhost utility to \
execute this action'

        source = str(self.element.source)
        urltool = getUtility(IURLTool)
        portal = urltool.getPortalObject()
        email_charset = portal.getProperty('email_charset')

        if not source:
            # no source provided, looking for the site wide from email
            # address
            from_address = portal.getProperty('email_from_address')
            if not from_address:
                raise ValueError, 'You must provide a source address for this\
action or enter an email in the portal properties'
            from_name = portal.getProperty('email_from_name')
            source = "%s <%s>" % (from_address, portal.email_from_address)

        obj = self.event.object
        event_title = obj.Title()
        event_url = obj.absolute_url()
        message = self.element.message.replace("${url}", event_url)
        message = message.replace("${title}", event_title)

        subject = self.element.subject.replace("${url}", event_url)
        subject = subject.replace("${title}", event_title)

        for email_recipient in recipients:
            mailhost.secureSend(message, email_recipient, source,
                                subject=subject, subtype='plain',
                                charset=email_charset, debug=False,
                                From=source)
        return True

class MailAddForm(AddForm):
    """
    An add form for the mail action
    """
    form_fields = form.FormFields(IMailAction)
    label = _(u"Add Mail action")
    description = _(u"A Mail action can mail different recipient.")
    form_name = _(u"Configure element")

    def create(self, data):
        a = MailAction()
        form.applyChanges(a, self.form_fields, data)
        return a

class MailEditForm(EditForm):
    """
    An edit form for the mail action
    """
    form_fields = form.FormFields(IMailAction)
    label = _(u"Edit Mail Action")
    description = _(u"A Mail action can mail different recipient.")
    form_name = _(u"Configure element")