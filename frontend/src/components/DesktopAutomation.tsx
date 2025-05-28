import React, { useState } from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import axios from 'axios';

const DesktopAutomation = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const formik = useFormik({
    initialValues: {
      appName: 'notepad',
      action: 'type',
      text: ''
    },
    validationSchema: Yup.object({
      appName: Yup.string().required('Required'),
      action: Yup.string().required('Required'),
      text: Yup.string().when('action', ([action], schema: Yup.StringSchema) => {
        return action === 'type'
        ? schema.required('Text is required for typing action')
        : schema;
}),



    }),
    onSubmit: async (values) => {
  setIsLoading(true);
  setError(null);

  try {
    // Create a new payload object manually
    const payload: { appName: string; action: string; text?: string } = {
    appName: values.appName,
    action: values.action,
};

  // Only add text if action is 'type'
  if (values.action === 'type') {
    payload.text = values.text;
  }


    const response = await axios.post('http://localhost:8000/api/desktop-automate', payload);
    setResult(response.data);
  } catch (err: any) {
    setError(err.response?.data?.detail || 'An error occurred');
  } finally {
    setIsLoading(false);
  }
},

  });

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-medium text-gray-900">Desktop Automation</h2>
        <p className="mt-1 text-sm text-gray-500">
          Automate desktop applications like Notepad.
        </p>
      </div>

      <form onSubmit={formik.handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="appName" className="block text-sm font-medium text-gray-700">
            Application
          </label>
          <select
            id="appName"
            name="appName"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.appName}
            className="mt-1 block w-full rounded-md border-gray-300 py-2 pl-3 pr-10 text-base focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
          >
            <option value="notepad">Notepad</option>
            <option value="wordpad">WordPad</option>
            <option value="calculator">Calculator</option>
          </select>
        </div>

        <div>
          <label htmlFor="action" className="block text-sm font-medium text-gray-700">
            Action
          </label>
          <select
            id="action"
            name="action"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.action}
            className="mt-1 block w-full rounded-md border-gray-300 py-2 pl-3 pr-10 text-base focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
          >
            <option value="type">Type Text</option>
            <option value="open">Open Application</option>
            <option value="close">Close Application</option>
          </select>
        </div>

        {formik.values.action === 'type' && (
          <div>
            <label htmlFor="text" className="block text-sm font-medium text-gray-700">
              Text to Type
            </label>
            <textarea
              id="text"
              name="text"
              rows={4}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.text}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              placeholder="Enter the text you want to type..."
            />
            {formik.touched.text && formik.errors.text ? (
              <p className="mt-1 text-sm text-red-600">{formik.errors.text}</p>
            ) : null}
          </div>
        )}

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isLoading}
            className="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50"
          >
            {isLoading ? 'Processing...' : 'Run Desktop Automation'}
          </button>
        </div>
      </form>

      {error && (
        <div className="rounded-md bg-red-50 p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Error</h3>
              <div className="mt-2 text-sm text-red-700">
                <p>{error}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {result && (
        <div className="rounded-md bg-green-50 p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-green-800">Success</h3>
              <div className="mt-2 text-sm text-green-700">
                <pre className="whitespace-pre-wrap">{JSON.stringify(result, null, 2)}</pre>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DesktopAutomation;
