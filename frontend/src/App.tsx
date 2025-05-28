import React, { useState } from 'react';
import { Tab } from '@headlessui/react';
import WebAutomation from './components/WebAutomation';
import DesktopAutomation from './components/DesktopAutomation';
import DocumentAutomation from './components/DocumentAutomation';

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(' ');
}

function App() {
  const [selectedIndex, setSelectedIndex] = useState(0);

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">Automation Dashboard</h1>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white rounded-lg shadow">
            <Tab.Group selectedIndex={selectedIndex} onChange={setSelectedIndex}>
              <Tab.List className="flex border-b border-gray-200">
                <Tab
                  className={({ selected }) =>
                    classNames(
                      'py-4 px-6 text-sm font-medium',
                      selected
                        ? 'border-b-2 border-indigo-500 text-indigo-600'
                        : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    )
                  }
                >
                  Web Automation
                </Tab>
                <Tab
                  className={({ selected }) =>
                    classNames(
                      'py-4 px-6 text-sm font-medium',
                      selected
                        ? 'border-b-2 border-indigo-500 text-indigo-600'
                        : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    )
                  }
                >
                  Desktop Automation
                </Tab>
                <Tab
                  className={({ selected }) =>
                    classNames(
                      'py-4 px-6 text-sm font-medium',
                      selected
                        ? 'border-b-2 border-indigo-500 text-indigo-600'
                        : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    )
                  }
                >
                  Document Automation
                </Tab>
              </Tab.List>
              <Tab.Panels className="p-6">
                <Tab.Panel>
                  <WebAutomation />
                </Tab.Panel>
                <Tab.Panel>
                  <DesktopAutomation />
                </Tab.Panel>
                <Tab.Panel>
                  <DocumentAutomation />
                </Tab.Panel>
              </Tab.Panels>
            </Tab.Group>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
