import React from 'react'
import { globalContext } from './globalContext'
import { Navigate } from 'react-router';

const ProtectedRoutes = ({children}) => {
  const {auth} = React.useContext(globalContext);

  return auth ? children : <Navigate to={'/login'} replace/>
}

export default ProtectedRoutes