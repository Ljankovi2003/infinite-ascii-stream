import React, { useEffect, useRef, useState } from 'react';
import { format } from 'date-fns';

const Terminal = () => {
  const terminalRef = useRef<HTMLDivElement>(null);
  const [displayedCode, setDisplayedCode] = useState<string[]>([]);
  const [currentTime, setCurrentTime] = useState(new Date());
  const status = 'ACTIVE';
  const [functions, setFunctions] = useState<string[]>([]);

  const statusColors = {
    ACTIVE: 'bg-green-500',
    SCANNING: 'bg-blue-500',
    PROCESSING: 'bg-yellow-500',
    ANALYZING: 'bg-purple-500'
  };

  // Fetch functions from backend
  const fetchFunctions = async () => {
    try {
      const response = await fetch('/api/functions');
      const data = await response.json();
      setFunctions(data); // Update state with fetched functions
    } catch (error) {
      console.error('Error fetching functions:', error);
    }
  };

  useEffect(() => {
    fetchFunctions(); // Fetch functions on component mount
  }, []);

  // Function to generate random code
  const generateCode = () => {
    if (functions.length === 0) return ''; // Return empty string if no functions
    return functions[Math.floor(Math.random() * functions.length)];
  };

  // Update current time every second
  useEffect(() => {
    const maxDisplayedLines = 50;
  
    const typingInterval = setInterval(() => {
      const currentCode = generateCode();
      if (!currentCode) return;
  
      let currentIndex = 0;  // Reset index for each new line
      let tempCode = '';
  
      const typeCharacter = () => {
        if (currentIndex < currentCode.length) {
          const randomDelay = Math.random() < 0.1;
          if (!randomDelay) {
            tempCode += currentCode[currentIndex];
            
            setDisplayedCode(prev => {
              const newArray = [...prev];
              if (newArray.length >= maxDisplayedLines) {
                newArray.shift();
              }
              if (newArray.length === 0) {
                newArray.push(tempCode);
              } else {
                newArray[newArray.length - 1] = tempCode;
              }
              return newArray;
            });
  
            currentIndex++;
            setTimeout(typeCharacter, 5);
          } else {
            setTimeout(typeCharacter, 10);
          }
        } else {
          setDisplayedCode(prev => {
            const newArray = [...prev, ''];
            return newArray.slice(-maxDisplayedLines);
          });
        }
      };
  
      typeCharacter();
    }, 4000);
  
    return () => clearInterval(typingInterval);
  }, [functions]);
  return (
    <div className="relative space-y-2 sm:space-y-4 mb-8">
      <div className="terminal-header p-2 sm:p-4 border border-white/5 rounded-lg flex items-center justify-between">
        <div className="flex items-center space-x-2 sm:space-x-3">
          <div className={`h-2 w-2 sm:h-3 sm:w-3 rounded-full ${statusColors[status]} animate-pulse status-glow`}></div>
          <span className="text-white/80 font-mono text-xs sm:text-sm glow">STATUS: {status}</span>
        </div>
        <div className="text-white/80 font-mono text-xs sm:text-sm glow">
          {format(currentTime, 'HH:mm:ss')}
        </div>
      </div>

      <div
        ref={terminalRef}
        className="terminal-body h-[calc(100vh-16rem)] sm:h-[calc(100vh-26rem)] overflow-y-auto overflow-x-hidden p-2 sm:p-4 border border-white/5 rounded-lg scrollbar-hide"
        style={{ scrollBehavior: 'smooth', msOverflowStyle: 'none', scrollbarWidth: 'none' }}
      >
        <style>
          {`
            .scrollbar-hide::-webkit-scrollbar {
              display: none;
            }
          `}
        </style>
        {displayedCode.map((code, index) => (
          <pre key={index} className="text-white/90 text-xs sm:text-sm font-mono mb-2 sm:mb-4 whitespace-pre hover:text-white/100 transition-colors">
            {code}
            {index === displayedCode.length - 1 && (
              <span className="animate-pulse inline-block w-1.5 sm:w-2 h-3 sm:h-4 bg-white/90 ml-1 glow">_</span>
            )}
          </pre>
        ))}
      </div>
    </div>
  );
};

export default Terminal;
