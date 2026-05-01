import { useState, useEffect } from 'react'
import axios from 'axios'
import { API_BASE } from '../config'

export default function Contacts() {
  const [contacts, setContacts] = useState([])
  const [form, setForm] = useState({ name: '', email: '' })

  useEffect(() => {
    fetchContacts()
  }, [])

  const fetchContacts = async () => {
    const res = await axios.get(`${API_BASE}/contacts`)
    setContacts(res.data)
  }

  const addContact = async () => {
    await axios.post(`${API_BASE}/contacts`, form)
    setForm({ name: '', email: '' })
    fetchContacts()
  }

  return (
    <div className="max-w-2xl mx-auto px-6 py-10">
      <h2 className="text-2xl font-bold mb-6">Trusted Contacts</h2>
      
      <div className="bg-gray-900 rounded-xl p-6 mb-6">
        <input
          value={form.name}
          onChange={(e) => setForm({...form, name: e.target.value})}
          placeholder="Name"
          className="w-full bg-gray-800 rounded-lg p-3 mb-3 text-white"
        />
       <input
          value={form.email}
          onChange={(e) => setForm({...form, email: e.target.value})}
          placeholder="Email address"
          type="email"
          className="w-full bg-gray-800 rounded-lg p-3 mb-3 text-white placeholder-gray-500 border border-gray-700"
        />
        <button onClick={addContact} className="bg-red-600 text-white px-6 py-2 rounded-lg">
          Add Contact
        </button>
      </div>

      {contacts.map(contact => (
        <div key={contact.id} className="bg-gray-900 rounded-lg p-4 mb-3">
          <p className="font-bold">{contact.name}</p>
          <p className="text-gray-400 text-sm">{contact.email}</p>
        </div>
      ))}
    </div>
  )
}