import React from "react";
import { Box } from "@mui/material";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import FormRegister from "./pages/FormRegister";
import FormLogin from "./pages/FormLogin";
import { AuthProvider } from "./contexts/AuthContext"; // Добавлено
import { ThemeProvider } from "./themes/RegistrationLoginFormThemeProvider";
import Header from "./components/Header";
import Footer from "./components/Footer";

const App = () => {
  return (
    <ThemeProvider>
      <AuthProvider>
        <Router>
          <Header />
          <Box sx={{ flex: 1, display: "flex", flexDirection: "column" }}>
            <Routes>
              <Route path="/register" element={<FormRegister />} />
              <Route path="/login" element={<FormLogin />} />
            </Routes>
          </Box>
          <Footer />
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
};

export default App;
