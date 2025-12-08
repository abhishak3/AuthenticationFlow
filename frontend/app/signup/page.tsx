'use client'

import { useReducer, useState } from "react";
import Link from "next/link";

import { SignupForm, Status } from "./signup.types";
import { isFormValid } from "./signup.helper";

export default function Page() {
  const initialState : SignupForm = {
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    confirm_password: ""
  }

  function reducer(state: SignupForm, action: Partial<SignupForm>) {
    return {
      ...state,
      ...action
    }
  }
  
  const [form, dispatch] = useReducer(reducer, initialState);
  const [status, setStatus] = useState<Status>(null);

  function onFormSubmit() {
    if (!isFormValid(form)) {
      setStatus('error');
      return;
    }

    const API_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

    setStatus('loading');

    fetch(`${API_URL}/auth/signup`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        firstName: form.firstName,
        lastName: form.lastName,
        email: form.email,
        password: form.password,
      })
    })
    .then(() => {
      dispatch(initialState);
      setStatus('success');
    })
    .catch(() => setStatus('error'));
  }

  return (
    <div className="flex flex-col gap-4">
      <form className="w-[400px] flex flex-col gap-8 border rounded-xl p-4">
        <div className="flex gap-4">
          <label className="w-20" htmlFor="fname">First Name:</label>
          <input
            className="border rounded-sm grow h-10 p-2"
            type="text"
            id="fname"
            value={form.firstName}
            onChange={(e) => dispatch({firstName: e.target.value})}
          />
        </div>
        <div className="flex gap-4">
          <label className="w-20" htmlFor="lname">Last Name:</label>
          <input
            className="border rounded-sm grow h-10 p-2"
            type="text"
            id="lname"
            value={form.lastName}
            onChange={(e) => dispatch({lastName: e.target.value})}
          />
        </div>
        <div className="flex gap-4">
          <label className="w-20" htmlFor="email">Email:</label>
          <input
            className="border rounded-sm grow h-10 p-2"
            type="email"
            id="email"
            value={form.email}
            onChange={(e) => dispatch({email: e.target.value})}
          />
        </div>
        <div className="flex gap-4">
          <label className="w-20" htmlFor="password">Password:</label>
          <input
            className="border rounded-sm grow h-10 p-2"
            type="password"
            id="password"
            value={form.password}
            onChange={(e) => dispatch({password: e.target.value})}
          />
        </div>
        <div className="flex gap-4">
          <label className="w-20" htmlFor="cpassword">Confirm Password:</label>
          <input
            className="border rounded-sm grow h-10 p-2"
            type="password"
            id="cpassword"
            value={form.confirm_password}
            onChange={(e) => dispatch({confirm_password: e.target.value})}
          />
        </div>
        <button
          className="bg-blue-500 p-1 cursor-pointer"
          type="button"
          onClick={onFormSubmit}
          disabled={status==='loading'}
        >
          {status === 'loading' ? "Submitting..." : "Submit"}
        </button>
        {status === 'error' && <span className="text-red-400">Form is not valid!</span>}
        {status === 'success' && <span className="text-green-400">User created successfully!</span>}
      </form>
      <span>Already a user? <Link className="underline text-blue-400" href="/login">Log In</Link></span>
    </div>
  );
}
