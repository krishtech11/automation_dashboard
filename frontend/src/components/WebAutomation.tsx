import React, { useState } from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import axios from 'axios';



const WebAutomation = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const formik = useFormik({
    initialValues: {
      url: '',
      username: '',
      password: '',
      searchQuery: ''
    },
    validationSchema: Yup.object({
      url: Yup.string().url('Invalid URL').required('Required'),
      username: Yup.string(),
      password: Yup.string(),
      searchQuery: Yup.string()
    }),
    onSubmit: async (values) => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await axios.post('http://localhost:8000/api/web-automate', {
          url: values.url,
          username: values.username || null,
          password: values.password || null,
          search_query: values.searchQuery || ''
        });

        setResult(response.data);
      } catch (err: any) {
        console.error("Backend error:", err);
        setError(err.response?.data?.message || 'An error occurred');
      } finally {
        setIsLoading(false);
      }
    },
  });

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-medium text-gray-900">Web Automation</h2>
        <p className="mt-1 text-sm text-gray-500">
          Automate website interactions like login, search, and form filling.
        </p>
      </div>

      <form onSubmit={formik.handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="url" className="block text-sm font-medium text-gray-700">
            Website URL *
          </label>
          <input
            type="url"
            id="url"
            name="url"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.url}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            placeholder="https://example.com"
          />
          {formik.touched.url && formik.errors.url ? (
            <p className="mt-1 text-sm text-red-600">{formik.errors.url}</p>
          ) : null}
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-gray-700">
              Username (if login required)
            </label>
            <input
              type="text"
              id="username"
              name="username"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.username}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              placeholder="username"
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              Password (if login required)
            </label>
            <input
              type="password"
              id="password"
              name="password"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.password}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              placeholder="••••••••"
            />
          </div>
        </div>

        <div>
          <label htmlFor="searchQuery" className="block text-sm font-medium text-gray-700">
            Search Query (optional)
          </label>
          <input
            type="text"
            id="searchQuery"
            name="searchQuery"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.searchQuery}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            placeholder="What are you looking for?"
          />
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isLoading}
            className="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50"
          >
            {isLoading ? 'Processing...' : 'Run Web Automation'}
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

export default WebAutomation;
