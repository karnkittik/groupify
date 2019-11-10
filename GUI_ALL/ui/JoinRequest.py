import setup
import tkinter as tk
from tkinter import ttk

from entities.request import *

from services.user import UserService


def JoinRequest(req: Request):
    popup = tk.Tk()
    popup.wm_title('Request to join group')
    label = ttk.Label(
        popup, text=req.fromUsername + ' would like to join your group. Accept?', font=("Helvetica", 10))
    label.pack(side='top', fill='x', pady=10)
    confirmBtn = ttk.Button(popup, text='Accept',
                            command=lambda: acceptRequest(popup, req))
    cancelBtn = ttk.Button(
        popup, text='Deny', command=lambda: denyRequest(popup, req))
    confirmBtn.pack()
    cancelBtn.pack()
    popup.mainloop()


def acceptRequest(popup, req: Request):
    popup.destroy()
    ackReq = Request(req.fromUsername, req.groupID, {
        'message': 'Accept join group request'
    })
    print('Sending Group Acknowledge Request')
    setup.net.sendGroupAcknowledgeRequest(ackReq)
    UserService.updateGroup(req.fromUsername, req.groupID)


def denyRequest(popup, req: Request):
    popup.destroy()
    req = Request(req.fromUsername, req.groupID, {
        'message': 'Deny join group requeset'
    })
    print('Sending Group Deny Request')
    setup.net.sendGroupDenyRequest(req)
