import React from 'react';
import { Wifi, WifiOff, Coins } from 'lucide-react';

export const Header = ({ isOnline, coins }) => {
  return (
    <div className="top-bar">
      <div className="server-status">
        {isOnline ? (
          <><div className="status-dot online"></div> Online</>
        ) : (
          <><div className="status-dot offline"></div> Offline</>
        )}
      </div>
      
      <div className="coin-display">
        <Coins size={16} className="text-yellow-400" />
        <span>{coins}</span>
      </div>
    </div>
  );
};