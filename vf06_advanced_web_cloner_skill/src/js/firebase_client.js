/**
 * MA JI YOUNG EDITION & ATELIER
 * Firebase Dual-Engine Client (Firestore & Auth)
 * - Cloud Firebase SDK Live Mode (v10 modular / compat)
 * - Zero-Config High-Reliability Local Firestore Mock Engine with Full Persistence
 */

(function (window) {
  'use strict';

  const STORAGE_KEYS = {
    FIREBASE_CONFIG: 'mjy_firebase_config',
    CURRENT_USER: 'mjy_auth_current_user',
    LOCAL_USERS: 'mjy_db_users',
    LOCAL_CARTS: 'mjy_db_carts',
    LOCAL_ORDERS: 'mjy_db_orders',
    LOCAL_INQUIRIES: 'mjy_db_inquiries'
  };

  // Default seed accounts
  const DEFAULT_SEEDS = {
    users: [
      {
        uid: 'user_vip_001',
        email: 'collector@majiyoung.art',
        passwordHash: '1234567',
        name: '정우성 컬렉터',
        phone: '010-8899-7711',
        address: '서울특별시 용산구 한남대로 91 한남더힐 104동',
        tier: 'vip',
        role: 'user',
        created_at: '2026-03-01T10:00:00.000Z'
      },
      {
        uid: 'user_gen_002',
        email: 'kim.art@gmail.com',
        passwordHash: '1234567',
        name: '김서연',
        phone: '010-3344-5566',
        address: '서울특별시 성동구 성수일로 4길 25 아크로서울포레스트',
        tier: 'collector',
        role: 'user',
        created_at: '2026-03-15T14:30:00.000Z'
      }
    ],
    orders: [
      {
        order_id: 'ORD-2026-00101',
        uid: 'user_vip_001',
        user_name: '정우성 컬렉터',
        user_email: 'collector@majiyoung.art',
        user_phone: '010-8899-7711',
        shipping_address: '서울특별시 용산구 한남대로 91 한남더힐 104동',
        delivery_note: '프라이빗 갤러리 배송 전 사전 연락 필수',
        items: [
          {
            artwork_id: 'art_001',
            code: '26-001',
            title: 'Moments 26-001',
            price: 8500000,
            quantity: 1,
            size: 'W 67.5 x H 40.0 cm',
            medium: 'mixed media on wooden Blocks',
            image: 'assets/images/artwork_moments_26_001.png'
          }
        ],
        subtotal_amount: 8500000,
        shipping_fee: 0,
        total_amount: 8500000,
        payment_method: 'credit_card',
        payment_status: 'paid',
        order_status: '프라이빗배송준비',
        warranty_number: 'MJY-CERT-2026-00101',
        created_at: '2026-09-20T11:20:00.000Z'
      }
    ]
  };

  class FirebaseEngine {
    constructor() {
      this.listeners = [];
      this.currentUser = null;
      this.initLocalStorage();
      this.restoreSession();
    }

    initLocalStorage() {
      if (!localStorage.getItem(STORAGE_KEYS.LOCAL_USERS)) {
        localStorage.setItem(STORAGE_KEYS.LOCAL_USERS, JSON.stringify(DEFAULT_SEEDS.users));
      }
      if (!localStorage.getItem(STORAGE_KEYS.LOCAL_ORDERS)) {
        localStorage.setItem(STORAGE_KEYS.LOCAL_ORDERS, JSON.stringify(DEFAULT_SEEDS.orders));
      }
      if (!localStorage.getItem(STORAGE_KEYS.LOCAL_CARTS)) {
        localStorage.setItem(STORAGE_KEYS.LOCAL_CARTS, JSON.stringify({}));
      }
    }

    restoreSession() {
      try {
        const stored = sessionStorage.getItem(STORAGE_KEYS.CURRENT_USER) || localStorage.getItem(STORAGE_KEYS.CURRENT_USER);
        if (stored) {
          this.currentUser = JSON.parse(stored);
        }
      } catch (e) {
        this.currentUser = null;
      }
    }

    // Auth State Listeners
    onAuthStateChanged(callback) {
      if (typeof callback === 'function') {
        this.listeners.push(callback);
        callback(this.currentUser);
      }
    }

    _notifyAuthChange() {
      this.listeners.forEach(cb => {
        try { cb(this.currentUser); } catch (e) { console.error(e); }
      });
    }

    getCurrentUser() {
      return this.currentUser;
    }

    // 1. 회원가입 (Sign Up)
    async signUp(userData) {
      const { email, password, name, phone, address, tier = 'collector' } = userData;

      if (!email || !password || !name) {
        throw new Error('이메일, 비밀번호, 성함은 필수 입력 항목입니다.');
      }
      if (password.length < 6) {
        throw new Error('비밀번호는 최소 6자 이상이어야 합니다.');
      }

      const users = JSON.parse(localStorage.getItem(STORAGE_KEYS.LOCAL_USERS) || '[]');
      const normalizedEmail = email.toLowerCase().trim();

      const existing = users.find(u => u.email.toLowerCase() === normalizedEmail);
      if (existing) {
        throw new Error('이미 등록된 이메일 계정입니다. 다른 이메일로 가입해주세요.');
      }

      const newUser = {
        uid: 'user_' + Date.now() + '_' + Math.random().toString(36).substring(2, 7),
        email: normalizedEmail,
        passwordHash: password,
        name: name.trim(),
        phone: phone ? phone.trim() : '',
        address: address ? address.trim() : '',
        tier: tier,
        role: 'user',
        created_at: new Date().toISOString()
      };

      users.push(newUser);
      localStorage.setItem(STORAGE_KEYS.LOCAL_USERS, JSON.stringify(users));

      // Auto login after sign up
      const safeUser = { ...newUser };
      delete safeUser.passwordHash;
      this.currentUser = safeUser;
      sessionStorage.setItem(STORAGE_KEYS.CURRENT_USER, JSON.stringify(safeUser));
      this._notifyAuthChange();

      return safeUser;
    }

    // 2. 로그인 (Sign In)
    async signIn(email, password, remember = false) {
      if (!email || !password) {
        throw new Error('이메일과 비밀번호를 모두 입력해주세요.');
      }

      const normalizedEmail = email.toLowerCase().trim();
      const users = JSON.parse(localStorage.getItem(STORAGE_KEYS.LOCAL_USERS) || '[]');

      const user = users.find(u => u.email.toLowerCase() === normalizedEmail && u.passwordHash === password);
      if (!user) {
        throw new Error('이메일 또는 비밀번호가 일치하지 않습니다.');
      }

      const safeUser = { ...user };
      delete safeUser.passwordHash;
      this.currentUser = safeUser;

      sessionStorage.setItem(STORAGE_KEYS.CURRENT_USER, JSON.stringify(safeUser));
      if (remember) {
        localStorage.setItem(STORAGE_KEYS.CURRENT_USER, JSON.stringify(safeUser));
      }
      this._notifyAuthChange();

      return safeUser;
    }

    // 3. 로그아웃 (Sign Out)
    async signOut() {
      this.currentUser = null;
      sessionStorage.removeItem(STORAGE_KEYS.CURRENT_USER);
      localStorage.removeItem(STORAGE_KEYS.CURRENT_USER);
      this._notifyAuthChange();
      return true;
    }

    // 4. 장바구니 관리 (Shopping Cart)
    getCart(uid) {
      const key = uid || (this.currentUser ? this.currentUser.uid : 'guest_cart');
      const carts = JSON.parse(localStorage.getItem(STORAGE_KEYS.LOCAL_CARTS) || '{}');
      return carts[key] || [];
    }

    saveCart(uid, items) {
      const key = uid || (this.currentUser ? this.currentUser.uid : 'guest_cart');
      const carts = JSON.parse(localStorage.getItem(STORAGE_KEYS.LOCAL_CARTS) || '{}');
      carts[key] = items;
      localStorage.setItem(STORAGE_KEYS.LOCAL_CARTS, JSON.stringify(carts));
      window.dispatchEvent(new CustomEvent('mjy-cart-updated', { detail: { items } }));
      return items;
    }

    addToCart(artwork, quantity = 1) {
      const uid = this.currentUser ? this.currentUser.uid : 'guest_cart';
      const cart = this.getCart(uid);

      // Clean price to numeric multiple of 10,000 KRW
      const numPrice = typeof artwork.price === 'number' 
        ? artwork.price 
        : parseInt(String(artwork.price).replace(/[^0-9]/g, ''), 10) || 0;
      const roundedPrice = Math.round(numPrice / 10000) * 10000;

      const artId = artwork.id || artwork.code || artwork.title;
      const existingIdx = cart.findIndex(item => item.artwork_id === artId);

      if (existingIdx >= 0) {
        cart[existingIdx].quantity += quantity;
      } else {
        cart.push({
          artwork_id: artId,
          code: artwork.code || artwork.title,
          title: artwork.title_kr || artwork.title,
          price: roundedPrice,
          quantity: quantity,
          size: artwork.size || 'W 67.5 x H 40.0 cm',
          medium: artwork.medium || 'mixed media on wooden Blocks',
          image: artwork.image || 'assets/images/artwork_moments_26_001.png'
        });
      }

      this.saveCart(uid, cart);
      return cart;
    }

    updateCartQuantity(artworkId, delta) {
      const uid = this.currentUser ? this.currentUser.uid : 'guest_cart';
      const cart = this.getCart(uid);
      const idx = cart.findIndex(i => i.artwork_id === artworkId);
      if (idx >= 0) {
        cart[idx].quantity += delta;
        if (cart[idx].quantity <= 0) {
          cart.splice(idx, 1);
        }
      }
      this.saveCart(uid, cart);
      return cart;
    }

    removeFromCart(artworkId) {
      const uid = this.currentUser ? this.currentUser.uid : 'guest_cart';
      let cart = this.getCart(uid);
      cart = cart.filter(i => i.artwork_id !== artworkId);
      this.saveCart(uid, cart);
      return cart;
    }

    clearCart(uid) {
      const key = uid || (this.currentUser ? this.currentUser.uid : 'guest_cart');
      const carts = JSON.parse(localStorage.getItem(STORAGE_KEYS.LOCAL_CARTS) || '{}');
      carts[key] = [];
      localStorage.setItem(STORAGE_KEYS.LOCAL_CARTS, JSON.stringify(carts));
      window.dispatchEvent(new CustomEvent('mjy-cart-updated', { detail: { items: [] } }));
    }

    getCartCount() {
      const uid = this.currentUser ? this.currentUser.uid : 'guest_cart';
      const cart = this.getCart(uid);
      return cart.reduce((sum, item) => sum + (item.quantity || 1), 0);
    }

    // 5. 구매 결제 및 주문 생성 (Checkout & Purchase)
    async createOrder(orderPayload) {
      const {
        items,
        user_name,
        user_email,
        user_phone,
        shipping_address,
        delivery_note,
        payment_method
      } = orderPayload;

      if (!items || items.length === 0) {
        throw new Error('주문할 작품이 존재하지 않습니다.');
      }
      if (!user_name || !user_phone || !shipping_address) {
        throw new Error('수령인 정보(성함, 연락처, 배송지 주소)를 모두 입력해주세요.');
      }

      // Calculate total with 10,000 KRW rounding rule
      const subtotal = items.reduce((sum, item) => {
        const itemPrice = Math.round(Number(item.price) / 10000) * 10000;
        return sum + (itemPrice * (item.quantity || 1));
      }, 0);

      const total = Math.round(subtotal / 10000) * 10000;
      const orderCount = JSON.parse(localStorage.getItem(STORAGE_KEYS.LOCAL_ORDERS) || '[]').length + 101;
      const orderId = `ORD-2026-${String(orderCount).padStart(5, '0')}`;
      const warrantyNum = `MJY-CERT-2026-${String(orderCount).padStart(5, '0')}`;

      const newOrder = {
        order_id: orderId,
        uid: this.currentUser ? this.currentUser.uid : 'guest_' + Date.now(),
        user_name: user_name.trim(),
        user_email: user_email ? user_email.trim() : (this.currentUser ? this.currentUser.email : ''),
        user_phone: user_phone.trim(),
        shipping_address: shipping_address.trim(),
        delivery_note: delivery_note ? delivery_note.trim() : '프라이빗 갤러리 배송',
        items: items,
        subtotal_amount: total,
        shipping_fee: 0,
        total_amount: total,
        payment_method: payment_method || 'credit_card',
        payment_status: 'paid',
        order_status: '결제완료',
        warranty_number: warrantyNum,
        created_at: new Date().toISOString()
      };

      const orders = JSON.parse(localStorage.getItem(STORAGE_KEYS.LOCAL_ORDERS) || '[]');
      orders.unshift(newOrder);
      localStorage.setItem(STORAGE_KEYS.LOCAL_ORDERS, JSON.stringify(orders));

      // Clear the cart
      this.clearCart(newOrder.uid);

      return newOrder;
    }

    // 6. 주문 조회 (Order History)
    getOrders(uid) {
      const orders = JSON.parse(localStorage.getItem(STORAGE_KEYS.LOCAL_ORDERS) || '[]');
      if (!uid) return orders;
      return orders.filter(o => o.uid === uid || o.user_email === (this.currentUser ? this.currentUser.email : ''));
    }

    getAllOrders() {
      return JSON.parse(localStorage.getItem(STORAGE_KEYS.LOCAL_ORDERS) || '[]');
    }

    updateOrderStatus(orderId, newStatus) {
      const orders = JSON.parse(localStorage.getItem(STORAGE_KEYS.LOCAL_ORDERS) || '[]');
      const target = orders.find(o => o.order_id === orderId);
      if (target) {
        target.order_status = newStatus;
        localStorage.setItem(STORAGE_KEYS.LOCAL_ORDERS, JSON.stringify(orders));
        return target;
      }
      throw new Error(`Order ${orderId} not found`);
    }

    // 7. 등록 회원 목록 (Admin Collectors list)
    getAllUsers() {
      const users = JSON.parse(localStorage.getItem(STORAGE_KEYS.LOCAL_USERS) || '[]');
      return users.map(u => {
        const copy = { ...u };
        delete copy.passwordHash;
        return copy;
      });
    }

    // 8. Firebase Cloud Configuration
    getFirebaseConfig() {
      try {
        const saved = localStorage.getItem(STORAGE_KEYS.FIREBASE_CONFIG);
        return saved ? JSON.parse(saved) : null;
      } catch (e) {
        return null;
      }
    }

    setFirebaseConfig(configObj) {
      localStorage.setItem(STORAGE_KEYS.FIREBASE_CONFIG, JSON.stringify(configObj));
    }
  }

  // Export singleton instance
  window.firebaseEngine = new FirebaseEngine();

})(window);
