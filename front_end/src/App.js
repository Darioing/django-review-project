import React from "react";
import { Box } from "@mui/material";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import FormRegister from "./pages/FormRegister";
import FormLogin from "./pages/FormLogin";
import MainPage from "./pages/MainPage";
import PlaceDetails from "./pages/Place";
import { AuthProvider } from "./contexts/AuthContext"; // Добавлено
import GlobalThemeProvider from "./themes/GlobalThemeProvider";

import Header from "./components/Header";
import Footer from "./components/Footer";

const App = () => {
  return (
    <GlobalThemeProvider>
      <AuthProvider>
        <Router>
          <Header />
          <Box sx={{ flex: 1, display: "flex", flexDirection: "column" }}>
            <Routes>
              <Route path="/" element={<MainPage />} />
              <Route path="/place/:slug" element={<PlaceDetails />} />
              <Route path="/register" element={<FormRegister />} />
              <Route path="/login" element={<FormLogin />} />
            </Routes>
          </Box>
          <Footer />
        </Router>
      </AuthProvider>
    </GlobalThemeProvider>
  );
};

export default App;
