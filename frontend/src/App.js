import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {

  const [selectedEmail, setSelectedEmail] = useState(null)
  const [emails, setEmails] = useState([])
  const [recipient, setRecipient] = useState('')
  const [subject, setSubject] = useState('')
  const [body, setBody] = useState('')
  const [sending, setSending] = useState(false)
  const [minimized, setMinimized] = useState(false)

  async function refreshEmails() {
    return axios.get('/api/emails').then(response => {
      setEmails(response.data)
      return response.data
    })
  }

  useEffect(() => {
    refreshEmails().then((data) => {
      setSelectedEmail(data[0].email_id)
    })
  }, []);

  function sendEmail() {
    const data = {recipient, subject, body}
    setSending(true)

    axios.post('/api/email', data).then(() => {
      refreshEmails()
      setRecipient('')
      setSubject('')
      setBody('')
      setSending(false)
    })
  }

  function renderEmail(email_id) {
    if (email_id != null) {
      const email_obj = emails.find(e => e.email_id == email_id)
      return (
        <div className="preview">
          <div className="preview-subject">{email_obj.subject}</div>
          <div className="preview-content">
            <div className="preview-sender">
              <div className="preview-sender-name">{email_obj.sender_name}</div>
              <div className="preview-sender-email">&#60;{email_obj.sender_email}&#62;</div>
            </div>
            <div className="preview-receiver">To: {email_obj.receiver}</div>
            <div className="preview-body">{email_obj.body}</div>
          </div>
        </div>
      )
    }
    else return null
  }

  return (
    <div className="container">

      <div className="column-left">
        <div className="list">
          {emails.map(email =>
              <div className={`list-obj ${email.email_id == selectedEmail ? "list-obj-selected" : ""}`} key={email.email_id} onClick={() => setSelectedEmail(email.email_id)}>
                <div className="list-obj-sender">{email.receiver}</div>
                <div className="list-obj-subject">{email.subject}</div>
                <div className="list-obj-body">{email.body}</div>
              </div>
          )}
        </div>
      </div>
      <div className="column-right">
        <div className="selected-email">
          {renderEmail(selectedEmail)}
        </div>
      </div>
      <div className="compose-container">
        <div className="compose-header">
          <div className="compose-header-text">{sending ? 'Sending...' : 'Compose email'}</div>
          { !minimized && !sending && <div className="compose-header-minimize" onClick={() => setMinimized(true)}>—</div> }
          { minimized && !sending && <div className="compose-header-minimize" onClick={() => setMinimized(false)}>＋</div> }
        </div>
        { !minimized && !sending && 
        <div>
          <div className="compose-input">
            <input className="compose-to" placeholder="Recipient" value={recipient} onChange={event => setRecipient(event.target.value)} />
            <input className="compose-subject" placeholder="Subject" value={subject} onChange={event => setSubject(event.target.value)} />
            <textarea className="compose-body" placeholder="Body" value={body} onChange={event => setBody(event.target.value)} />
          </div>
          <div className="compose-footer">
            <div className="compose-button" onClick={() => sendEmail()}>Send</div>
          </div>
        </div>
        }
      </div>

    </div>
  );
}

export default App;
