    $FUNC $method
    public static void $method($parameters) {
        class $methodCB {
            public void successCB(String result) {
                System.out.println("successCB: " + result);
            }
            public void errorCB(String message) {
                System.out.println("errorCB: " + message);
            }
        }

    }
    $ENDFUNC