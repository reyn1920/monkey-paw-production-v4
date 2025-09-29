import { initializeApp, FirebaseApp } from 'firebase/app';
import { 
  getAuth, 
  Auth, 
  signInWithEmailAndPassword, 
  createUserWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  User,
  GoogleAuthProvider,
  signInWithPopup,
  sendPasswordResetEmail,
  updateProfile
} from 'firebase/auth';
import { 
  getFirestore, 
  Firestore, 
  collection, 
  doc, 
  setDoc, 
  getDoc, 
  updateDoc, 
  deleteDoc, 
  onSnapshot,
  query,
  where,
  orderBy,
  Timestamp,
  increment
} from 'firebase/firestore';
import { 
  getStorage, 
  FirebaseStorage, 
  ref, 
  uploadBytes, 
  getDownloadURL, 
  deleteObject,
  listAll,
  getMetadata
} from 'firebase/storage';
import { 
  getFunctions, 
  Functions, 
  httpsCallable,
  connectFunctionsEmulator
} from 'firebase/functions';

// Browser-compatible EventEmitter replacement
class BrowserEventEmitter {
  private listeners: Map<string, Function[]> = new Map();

  on(event: string, listener: Function): void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event)!.push(listener);
  }

  emit(event: string, ...args: any[]): void {
    const eventListeners = this.listeners.get(event);
    if (eventListeners) {
      eventListeners.forEach(listener => {
        try {
          listener(...args);
        } catch (error) {
          console.error(`Error in event listener for ${event}:`, error);
        }
      });
    }
  }

  off(event: string, listener: Function): void {
    const eventListeners = this.listeners.get(event);
    if (eventListeners) {
      const index = eventListeners.indexOf(listener);
      if (index > -1) {
        eventListeners.splice(index, 1);
      }
    }
  }

  removeAllListeners(event?: string): void {
    if (event) {
      this.listeners.delete(event);
    } else {
      this.listeners.clear();
    }
  }
}

export interface FirebaseConfig {
  apiKey: string;
  authDomain: string;
  projectId: string;
  storageBucket: string;
  messagingSenderId: string;
  appId: string;
  measurementId?: string;
}

export interface CloudFunction {
  name: string;
  region: string;
  runtime: string;
  status: 'active' | 'inactive' | 'error';
  lastDeployed: string;
  memoryAllocation: number;
  timeout: number;
  environmentVariables: { [key: string]: string };
}

export interface HostingConfig {
  site: string;
  target?: string;
  public: string;
  ignore: string[];
  rewrites: Array<{
    source: string;
    destination?: string;
    function?: string;
  }>;
  headers: Array<{
    source: string;
    headers: Array<{
      key: string;
      value: string;
    }>;
  }>;
}

export interface DeploymentResult {
  success: boolean;
  deploymentId: string;
  url?: string;
  functions?: string[];
  errors: string[];
  warnings: string[];
  deployTime: number;
}

export interface AnalyticsData {
  pageViews: number;
  uniqueUsers: number;
  sessionDuration: number;
  bounceRate: number;
  topPages: Array<{ page: string; views: number }>;
  userDemographics: {
    countries: Array<{ country: string; users: number }>;
    devices: Array<{ device: string; users: number }>;
  };
}

export interface ProjectData {
  id: string;
  name: string;
  description: string;
  files: { [key: string]: string };
  metadata: {
    createdAt: Timestamp;
    updatedAt: Timestamp;
    owner: string;
    collaborators: string[];
    tags: string[];
    framework: string;
  };
  integrations: {
    cursor: boolean;
    boltdiy: boolean;
    traeai: boolean;
    firebase: boolean;
    vscode: boolean;
    windsurf: boolean;
  };
}

export interface UserProfile {
  uid: string;
  email: string;
  displayName?: string;
  photoURL?: string;
  projects: string[];
  integrations: {
    cursor?: { connected: boolean; apiKey?: string; projectId?: string };
    boltdiy?: { connected: boolean; token?: string; deploymentUrl?: string };
    traeai?: { connected: boolean; apiKey?: string; analysisEnabled?: boolean };
  };
  preferences: {
    theme: 'light' | 'dark';
    notifications: boolean;
    autoSync: boolean;
    analyticsEnabled: boolean;
    backupFrequency: 'daily' | 'weekly' | 'monthly';
  };
  subscription: {
    plan: 'free' | 'pro' | 'enterprise';
    status: 'active' | 'cancelled' | 'expired';
    expiresAt?: Timestamp;
  };
  usage: {
    storageUsed: number;
    functionsInvoked: number;
    hostingBandwidth: number;
    lastActivity: Timestamp;
  };
}

export class FirebaseService extends BrowserEventEmitter {
  private app: FirebaseApp | null = null;
  private auth: Auth | null = null;
  private db: Firestore | null = null;
  private storage: FirebaseStorage | null = null;
  private functions: Functions | null = null;
  private currentUser: User | null = null;
  private authStateListeners: ((user: User | null) => void)[] = [];
  private isEmulatorMode: boolean = false;

  constructor() {
    super()
    this.setupAuthStateListener();
  }

  // Initialize Firebase with configuration
  async initialize(config: FirebaseConfig, useEmulator: boolean = false): Promise<{ success: boolean; error?: string }> {
    try {
      this.app = initializeApp(config);
      this.auth = getAuth(this.app);
      this.db = getFirestore(this.app);
      this.storage = getStorage(this.app);
      this.functions = getFunctions(this.app);
      this.isEmulatorMode = useEmulator;

      // Connect to emulators if in development mode
      if (useEmulator && process.env.NODE_ENV === 'development') {
        try {
          connectFunctionsEmulator(this.functions, 'localhost', 5001);
          console.log('Connected to Firebase Functions emulator');
        } catch (error) {
          console.warn('Failed to connect to Functions emulator:', error);
        }
      }
      
      this.emit('initialized', { config, useEmulator });
      return { success: true };
    } catch (error: any) {
      console.error('Firebase initialization failed:', error);
      this.emit('initializationError', error);
      return { success: false, error: error.message };
    }
  }

  // Authentication methods
  async signIn(email: string, password: string): Promise<{ success: boolean; user?: User; error?: string }> {
    if (!this.auth) {
      return { success: false, error: 'Firebase not initialized' };
    }

    try {
      const userCredential = await signInWithEmailAndPassword(this.auth, email, password);
      this.currentUser = userCredential.user;
      this.emit('userSignedIn', userCredential.user);
      return { success: true, user: userCredential.user };
    } catch (error: any) {
      this.emit('signInError', error);
      return { success: false, error: error.message };
    }
  }

  async signInWithGoogle(): Promise<{ success: boolean; user?: User; error?: string }> {
    if (!this.auth) {
      return { success: false, error: 'Firebase not initialized' };
    }

    try {
      const provider = new GoogleAuthProvider();
      provider.addScope('profile');
      provider.addScope('email');
      
      const userCredential = await signInWithPopup(this.auth, provider);
      this.currentUser = userCredential.user;
      
      // Create or update user profile
      await this.createUserProfile(userCredential.user);
      
      this.emit('userSignedIn', userCredential.user);
      return { success: true, user: userCredential.user };
    } catch (error: any) {
      this.emit('signInError', error);
      return { success: false, error: error.message };
    }
  }

  async signUp(email: string, password: string, displayName?: string): Promise<{ success: boolean; user?: User; error?: string }> {
    if (!this.auth) {
      return { success: false, error: 'Firebase not initialized' };
    }

    try {
      const userCredential = await createUserWithEmailAndPassword(this.auth, email, password);
      
      // Update profile with display name if provided
      if (displayName) {
        await updateProfile(userCredential.user, { displayName });
      }
      
      this.currentUser = userCredential.user;
      await this.createUserProfile(userCredential.user);
      
      this.emit('userSignedUp', userCredential.user);
      return { success: true, user: userCredential.user };
    } catch (error: any) {
      this.emit('signUpError', error);
      return { success: false, error: error.message };
    }
  }

  async resetPassword(email: string): Promise<{ success: boolean; error?: string }> {
    if (!this.auth) {
      return { success: false, error: 'Firebase not initialized' };
    }

    try {
      await sendPasswordResetEmail(this.auth, email);
      this.emit('passwordResetSent', { email });
      return { success: true };
    } catch (error: any) {
      this.emit('passwordResetError', error);
      return { success: false, error: error.message };
    }
  }

  async signOutUser(): Promise<boolean> {
    if (!this.auth) return false;

    try {
      await signOut(this.auth);
      this.currentUser = null;
      this.emit('userSignedOut');
      return true;
    } catch (error: any) {
      console.error('Sign out failed:', error);
      this.emit('signOutError', error);
      return false;
    }
  }

  // Alias for signOutUser to match UnifiedAuthService expectations
  async signOut(): Promise<boolean> {
    return this.signOutUser();
  }

  // Cloud Functions
  async deployFunction(
    functionName: string, 
    code: string, 
    runtime: string = 'nodejs18',
    environmentVariables?: { [key: string]: string }
  ): Promise<{ success: boolean; error?: string }> {
    if (!this.functions) {
      return { success: false, error: 'Firebase Functions not initialized' };
    }

    try {
      const deployFunction = httpsCallable(this.functions, 'deployCloudFunction');
      const result = await deployFunction({
        name: functionName,
        code,
        runtime,
        environmentVariables: environmentVariables || {}
      });

      this.emit('functionDeployed', { functionName, result });
      return { success: true };
    } catch (error: any) {
      this.emit('functionDeployError', { functionName, error });
      return { success: false, error: error.message };
    }
  }

  async invokeFunction(functionName: string, data?: any): Promise<{ success: boolean; result?: any; error?: string }> {
    if (!this.functions) {
      return { success: false, error: 'Firebase Functions not initialized' };
    }

    try {
      const cloudFunction = httpsCallable(this.functions, functionName);
      const result = await cloudFunction(data);
      
      this.emit('functionInvoked', { functionName, data, result });
      return { success: true, result: result.data };
    } catch (error: any) {
      this.emit('functionInvokeError', { functionName, error });
      return { success: false, error: error.message };
    }
  }

  async listFunctions(): Promise<CloudFunction[]> {
    if (!this.functions) {
      throw new Error('Firebase Functions not initialized');
    }

    try {
      const listFunctions = httpsCallable(this.functions, 'listCloudFunctions');
      const result = await listFunctions();
      return result.data as CloudFunction[];
    } catch (error: any) {
      throw new Error(`Failed to list functions: ${error.message}`);
    }
  }

  async deleteFunction(functionName: string): Promise<boolean> {
    if (!this.functions) {
      return false;
    }

    try {
      const deleteFunction = httpsCallable(this.functions, 'deleteCloudFunction');
      await deleteFunction({ name: functionName });
      
      this.emit('functionDeleted', { functionName });
      return true;
    } catch (error: any) {
      this.emit('functionDeleteError', { functionName, error });
      return false;
    }
  }

  // Hosting Services
  async deployToHosting(
    files: { [path: string]: string },
    config: HostingConfig
  ): Promise<DeploymentResult> {
    if (!this.functions) {
      throw new Error('Firebase Functions not initialized');
    }

    const startTime = Date.now();

    try {
      const deployToHosting = httpsCallable(this.functions, 'deployToHosting');
      const result = await deployToHosting({ files, config });
      
      const deploymentResult: DeploymentResult = {
        success: true,
        deploymentId: (result.data as any).deploymentId,
        url: (result.data as any).url,
        errors: [],
        warnings: (result.data as any).warnings || [],
        deployTime: Date.now() - startTime
      };

      this.emit('hostingDeployed', deploymentResult);
      return deploymentResult;
    } catch (error: any) {
      const deploymentResult: DeploymentResult = {
        success: false,
        deploymentId: '',
        errors: [error.message],
        warnings: [],
        deployTime: Date.now() - startTime
      };

      this.emit('hostingDeployError', deploymentResult);
      return deploymentResult;
    }
  }

  async getHostingStatus(site: string): Promise<{ 
    status: 'active' | 'inactive' | 'error';
    url?: string;
    lastDeployed?: string;
    version?: string;
  }> {
    if (!this.functions) {
      throw new Error('Firebase Functions not initialized');
    }

    try {
      const getHostingStatus = httpsCallable(this.functions, 'getHostingStatus');
      const result = await getHostingStatus({ site });
      return result.data as { 
        status: 'active' | 'inactive' | 'error';
        url?: string;
        lastDeployed?: string;
        version?: string;
      };
    } catch (error: any) {
      throw new Error(`Failed to get hosting status: ${error.message}`);
    }
  }

  async rollbackHosting(site: string, version: string): Promise<boolean> {
    if (!this.functions) {
      return false;
    }

    try {
      const rollbackHosting = httpsCallable(this.functions, 'rollbackHosting');
      await rollbackHosting({ site, version });
      
      this.emit('hostingRolledBack', { site, version });
      return true;
    } catch (error: any) {
      this.emit('hostingRollbackError', { site, version, error });
      return false;
    }
  }

  // Analytics
  async getAnalytics(dateRange: { start: string; end: string }): Promise<AnalyticsData> {
    if (!this.functions) {
      throw new Error('Firebase Functions not initialized');
    }

    try {
      const getAnalytics = httpsCallable(this.functions, 'getAnalytics');
      const result = await getAnalytics(dateRange);
      return result.data as AnalyticsData;
    } catch (error: any) {
      throw new Error(`Failed to get analytics: ${error.message}`);
    }
  }

  async trackEvent(eventName: string, parameters: { [key: string]: any }): Promise<boolean> {
    if (!this.functions) {
      return false;
    }

    try {
      const trackEvent = httpsCallable(this.functions, 'trackEvent');
      await trackEvent({ eventName, parameters });
      
      this.emit('eventTracked', { eventName, parameters });
      return true;
    } catch (error: any) {
      this.emit('eventTrackError', { eventName, parameters, error });
      return false;
    }
  }

  // User profile management
  async createUserProfile(user: User): Promise<boolean> {
    if (!this.db) return false;

    try {
      const userProfile: UserProfile = {
        uid: user.uid,
        email: user.email || '',
        displayName: user.displayName || undefined,
        photoURL: user.photoURL || undefined,
        projects: [],
        integrations: {},
        preferences: {
          theme: 'light',
          notifications: true,
          autoSync: true,
          analyticsEnabled: true,
          backupFrequency: 'weekly'
        },
        subscription: {
          plan: 'free',
          status: 'active'
        },
        usage: {
          storageUsed: 0,
          functionsInvoked: 0,
          hostingBandwidth: 0,
          lastActivity: Timestamp.now()
        }
      };

      await setDoc(doc(this.db, 'users', user.uid), userProfile);
      this.emit('userProfileCreated', userProfile);
      return true;
    } catch (error) {
      console.error('Failed to create user profile:', error);
      this.emit('userProfileError', error);
      return false;
    }
  }

  async getUserProfile(uid: string): Promise<UserProfile | null> {
    if (!this.db) return null;

    try {
      const docRef = doc(this.db, 'users', uid);
      const docSnap = await getDoc(docRef);
      
      if (docSnap.exists()) {
        return docSnap.data() as UserProfile;
      }
      return null;
    } catch (error) {
      console.error('Failed to get user profile:', error);
      return null;
    }
  }

  async updateUserProfile(uid: string, updates: Partial<UserProfile>): Promise<boolean> {
    if (!this.db) return false;

    try {
      const docRef = doc(this.db, 'users', uid);
      await updateDoc(docRef, { 
        ...updates, 
        'usage.lastActivity': Timestamp.now() 
      });
      
      this.emit('userProfileUpdated', { uid, updates });
      return true;
    } catch (error) {
      console.error('Failed to update user profile:', error);
      this.emit('userProfileUpdateError', { uid, error });
      return false;
    }
  }

  async updateUserUsage(uid: string, usageType: 'storage' | 'functions' | 'bandwidth', amount: number): Promise<boolean> {
    if (!this.db) return false;

    try {
      const docRef = doc(this.db, 'users', uid);
      const updateField = `usage.${usageType === 'storage' ? 'storageUsed' : 
                                   usageType === 'functions' ? 'functionsInvoked' : 'hostingBandwidth'}`;
      
      await updateDoc(docRef, {
        [updateField]: increment(amount),
        'usage.lastActivity': Timestamp.now()
      });
      
      this.emit('userUsageUpdated', { uid, usageType, amount });
      return true;
    } catch (error) {
      console.error('Failed to update user usage:', error);
      return false;
    }
  }

  // Project management
  async createProject(projectData: Omit<ProjectData, 'id' | 'metadata'>): Promise<string | null> {
    if (!this.db || !this.currentUser) return null;

    try {
      const projectId = `project_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      const project: ProjectData = {
        ...projectData,
        id: projectId,
        metadata: {
          createdAt: Timestamp.now(),
          updatedAt: Timestamp.now(),
          owner: this.currentUser.uid,
          collaborators: [],
          tags: [],
          framework: 'react'
        }
      };

      await setDoc(doc(this.db, 'projects', projectId), project);
      
      // Add project to user's project list
      const userProfile = await this.getUserProfile(this.currentUser.uid);
      if (userProfile) {
        await this.updateUserProfile(this.currentUser.uid, {
          projects: [...userProfile.projects, projectId]
        });
      }

      return projectId;
    } catch (error) {
      console.error('Failed to create project:', error);
      return null;
    }
  }

  async getProject(projectId: string): Promise<ProjectData | null> {
    if (!this.db) return null;

    try {
      const docRef = doc(this.db, 'projects', projectId);
      const docSnap = await getDoc(docRef);
      
      if (docSnap.exists()) {
        return docSnap.data() as ProjectData;
      }
      return null;
    } catch (error) {
      console.error('Failed to get project:', error);
      return null;
    }
  }

  async updateProject(projectId: string, updates: Partial<ProjectData>): Promise<boolean> {
    if (!this.db) return false;

    try {
      const docRef = doc(this.db, 'projects', projectId);
      await updateDoc(docRef, {
        ...updates,
        'metadata.updatedAt': Timestamp.now()
      });
      return true;
    } catch (error) {
      console.error('Failed to update project:', error);
      return false;
    }
  }

  async deleteProject(projectId: string): Promise<boolean> {
    if (!this.db || !this.currentUser) return false;

    try {
      // Remove from user's project list
      const userProfile = await this.getUserProfile(this.currentUser.uid);
      if (userProfile) {
        await this.updateUserProfile(this.currentUser.uid, {
          projects: userProfile.projects.filter(id => id !== projectId)
        });
      }

      // Delete project document
      await deleteDoc(doc(this.db, 'projects', projectId));
      return true;
    } catch (error) {
      console.error('Failed to delete project:', error);
      return false;
    }
  }

  // Real-time synchronization
  subscribeToProject(projectId: string, callback: (project: ProjectData | null) => void): () => void {
    if (!this.db) return () => {};

    const docRef = doc(this.db, 'projects', projectId);
    return onSnapshot(docRef, (doc: any) => {
      if (doc.exists()) {
        callback(doc.data() as ProjectData);
      } else {
        callback(null);
      }
    });
  }

  subscribeToUserProjects(uid: string, callback: (projects: ProjectData[]) => void): () => void {
    if (!this.db) return () => {};

    const q = query(
      collection(this.db, 'projects'),
      where('metadata.owner', '==', uid),
      orderBy('metadata.updatedAt', 'desc')
    );

    return onSnapshot(q, (querySnapshot: any) => {
      const projects: ProjectData[] = [];
      querySnapshot.forEach((doc: any) => {
        projects.push(doc.data() as ProjectData);
      });
      callback(projects);
    });
  }

  // File storage
  async uploadFile(projectId: string, fileName: string, file: Blob): Promise<string | null> {
    if (!this.storage) return null;

    try {
      const storageRef = ref(this.storage, `projects/${projectId}/${fileName}`);
      const snapshot = await uploadBytes(storageRef, file);
      const downloadURL = await getDownloadURL(snapshot.ref);
      return downloadURL;
    } catch (error) {
      console.error('Failed to upload file:', error);
      return null;
    }
  }

  async deleteFile(projectId: string, fileName: string): Promise<boolean> {
    if (!this.storage) return false;

    try {
      const storageRef = ref(this.storage, `projects/${projectId}/${fileName}`);
      await deleteObject(storageRef);
      return true;
    } catch (error) {
      console.error('Failed to delete file:', error);
      return false;
    }
  }

  // Enhanced integration methods for cross-platform sync
  async syncWithCursor(projectId: string, cursorData: any): Promise<boolean> {
    try {
      if (!this.db) {
        throw new Error('Firestore not initialized');
      }

      const projectRef = doc(this.db, 'projects', projectId);
      const projectDoc = await getDoc(projectRef);
      
      if (!projectDoc.exists()) {
        console.error('Project not found:', projectId);
        return false;
      }

      // Update project with Cursor sync data
      await updateDoc(projectRef, {
        'integrations.cursor': true,
        'metadata.updatedAt': Timestamp.now(),
        files: cursorData.files || {},
        ...(cursorData.metadata && { 'metadata.framework': cursorData.metadata.framework })
      });

      // Emit sync event
      this.emit('cursor-sync', { projectId, data: cursorData });
      
      console.log('Successfully synced with Cursor for project:', projectId);
      return true;
    } catch (error) {
      console.error('Error syncing with Cursor:', error);
      return false;
    }
  }

  async syncWithBoltDiy(projectId: string, boltData: any): Promise<boolean> {
    try {
      if (!this.db) {
        throw new Error('Firestore not initialized');
      }

      const projectRef = doc(this.db, 'projects', projectId);
      const projectDoc = await getDoc(projectRef);
      
      if (!projectDoc.exists()) {
        console.error('Project not found:', projectId);
        return false;
      }

      // Update project with Bolt.diy sync data
      await updateDoc(projectRef, {
        'integrations.boltdiy': true,
        'metadata.updatedAt': Timestamp.now(),
        files: boltData.files || {},
        ...(boltData.deploymentUrl && { deploymentUrl: boltData.deploymentUrl })
      });

      // Emit sync event
      this.emit('boltdiy-sync', { projectId, data: boltData });
      
      console.log('Successfully synced with Bolt.diy for project:', projectId);
      return true;
    } catch (error) {
      console.error('Error syncing with Bolt.diy:', error);
      return false;
    }
  }

  async syncWithTraeAI(projectId: string, traeData: any): Promise<boolean> {
    try {
      if (!this.db) {
        throw new Error('Firestore not initialized');
      }

      const projectRef = doc(this.db, 'projects', projectId);
      const projectDoc = await getDoc(projectRef);
      
      if (!projectDoc.exists()) {
        console.error('Project not found:', projectId);
        return false;
      }

      // Update project with Trae.AI sync data
      await updateDoc(projectRef, {
        'integrations.traeai': true,
        'metadata.updatedAt': Timestamp.now(),
        files: traeData.files || {},
        ...(traeData.analysis && { analysis: traeData.analysis })
      });

      // Emit sync event
      this.emit('traeai-sync', { projectId, data: traeData });
      
      console.log('Successfully synced with Trae.AI for project:', projectId);
      return true;
    } catch (error) {
      console.error('Error syncing with Trae.AI:', error);
      return false;
    }
  }

  // NEW: Unified multi-platform sync method
  async syncAllPlatformsUnified(projectId: string, platformData: {
    cursor?: any;
    boltdiy?: any;
    traeai?: any;
    firebase?: any;
  }): Promise<{
    cursor: boolean;
    boltdiy: boolean;
    traeai: boolean;
    firebase: boolean;
    errors: string[];
  }> {
    const results = {
      cursor: false,
      boltdiy: false,
      traeai: false,
      firebase: true, // Firebase is always available as the hub
      errors: [] as string[]
    };

    try {
      // Get project data
      const project = await this.getProject(projectId);
      if (!project) {
        results.errors.push('Project not found');
        return results;
      }

      // Sync with all platforms simultaneously (not exclusively)
      const syncPromises = [];

      if (platformData.cursor) {
        syncPromises.push(
          this.syncWithCursor(projectId, platformData.cursor)
            .then(success => { results.cursor = success; })
            .catch(error => { results.errors.push(`Cursor sync failed: ${error.message}`); })
        );
      }

      if (platformData.boltdiy) {
        syncPromises.push(
          this.syncWithBoltDiy(projectId, platformData.boltdiy)
            .then(success => { results.boltdiy = success; })
            .catch(error => { results.errors.push(`Bolt.diy sync failed: ${error.message}`); })
        );
      }

      if (platformData.traeai) {
        syncPromises.push(
          this.syncWithTraeAI(projectId, platformData.traeai)
            .then(success => { results.traeai = success; })
            .catch(error => { results.errors.push(`Trae.ai sync failed: ${error.message}`); })
        );
      }

      // Wait for all sync operations to complete
      await Promise.allSettled(syncPromises);

      // Update project with unified sync results
      await this.updateProject(projectId, {
        integrations: {
          cursor: results.cursor,
          boltdiy: results.boltdiy,
          traeai: results.traeai,
          firebase: results.firebase,
          vscode: project.integrations?.vscode || false,
          windsurf: project.integrations?.windsurf || false
        }
      });

      this.emit('allPlatformsSyncedUnified', { projectId, results });
      return results;
    } catch (error: any) {
      results.errors.push(`Unified sync orchestration failed: ${error.message}`);
      this.emit('allPlatformsSyncError', { projectId, error });
      return results;
    }
  }

  // NEW: Real-time cross-platform event broadcasting
  async broadcastToAllPlatforms(projectId: string, event: {
    type: 'file_change' | 'project_update' | 'deployment' | 'analysis_complete';
    data: any;
    source: 'cursor' | 'boltdiy' | 'traeai' | 'firebase';
  }): Promise<boolean> {
    if (!this.db) return false;

    try {
      // Store the event in Firestore for real-time distribution
      const eventRef = doc(this.db, 'platform_events', `${projectId}_${Date.now()}`);
      await setDoc(eventRef, {
        projectId,
        ...event,
        timestamp: Timestamp.now(),
        processed: false
      });

      // Emit to local listeners
      this.emit('crossPlatformEvent', { projectId, event });
      
      return true;
    } catch (error: any) {
      console.error('Failed to broadcast cross-platform event:', error);
      return false;
    }
  }

  // NEW: Get unified integration status for all platforms
  async getUnifiedIntegrationStatus(projectId: string): Promise<{
    platforms: {
      cursor: { connected: boolean; lastSync?: string; status?: string };
      boltdiy: { connected: boolean; lastSync?: string; deploymentUrl?: string };
      traeai: { connected: boolean; lastSync?: string; analysisStatus?: string };
      firebase: { connected: boolean; lastSync?: string };
    };
    overallHealth: 'healthy' | 'warning' | 'error';
    activeConnections: number;
  }> {
    try {
      if (!this.db) {
        throw new Error('Firestore not initialized');
      }

      const projectRef = doc(this.db, 'projects', projectId);
      const projectDoc = await getDoc(projectRef);
      
      if (!projectDoc.exists()) {
        throw new Error('Project not found');
      }

      const projectData = projectDoc.data() as ProjectData;
      const integrations = projectData.integrations;

      const platforms = {
        cursor: {
          connected: integrations.cursor || false,
          lastSync: new Date().toISOString(),
          status: integrations.cursor ? 'active' : 'inactive'
        },
        boltdiy: {
          connected: integrations.boltdiy || false,
          lastSync: new Date().toISOString(),
          deploymentUrl: 'https://bolt.diy/deploy'
        },
        traeai: {
          connected: integrations.traeai || false,
          lastSync: new Date().toISOString(),
          analysisStatus: integrations.traeai ? 'complete' : 'pending'
        },
        firebase: {
          connected: integrations.firebase || false,
          lastSync: new Date().toISOString()
        }
      };

      const activeConnections = Object.values(platforms).filter(p => p.connected).length;
      
      let overallHealth: 'healthy' | 'warning' | 'error' = 'healthy';
      if (activeConnections === 0) {
        overallHealth = 'error';
      } else if (activeConnections < 3) {
        overallHealth = 'warning';
      }

      return {
        platforms,
        overallHealth,
        activeConnections
      };
    } catch (error) {
      console.error('Error getting unified integration status:', error);
      return {
        platforms: {
          cursor: { connected: false },
          boltdiy: { connected: false },
          traeai: { connected: false },
          firebase: { connected: false }
        },
        overallHealth: 'error',
        activeConnections: 0
      };
    }
  }

  // Backup and restore functionality
  async createProjectBackup(projectId: string): Promise<{ success: boolean; backupId?: string; error?: string }> {
    if (!this.db || !this.storage) {
      return { success: false, error: 'Firebase not initialized' };
    }

    try {
      const project = await this.getProject(projectId);
      if (!project) {
        return { success: false, error: 'Project not found' };
      }

      const backupId = `backup_${projectId}_${Date.now()}`;
      const backupData = {
        ...project,
        backupId,
        createdAt: Timestamp.now()
      };

      // Store backup in Firestore
      await setDoc(doc(this.db, 'backups', backupId), backupData);

      // Store backup files in Storage
      const backupRef = ref(this.storage, `backups/${backupId}/project.json`);
      const backupBlob = new Blob([JSON.stringify(backupData, null, 2)], { type: 'application/json' });
      await uploadBytes(backupRef, backupBlob);

      // Update user usage
      if (this.currentUser) {
        await this.updateUserUsage(this.currentUser.uid, 'storage', backupBlob.size);
      }

      this.emit('backupCreated', { projectId, backupId });
      return { success: true, backupId };
    } catch (error: any) {
      this.emit('backupError', { projectId, error });
      return { success: false, error: error.message };
    }
  }

  async restoreProjectFromBackup(backupId: string): Promise<{ success: boolean; projectId?: string; error?: string }> {
    if (!this.db) {
      return { success: false, error: 'Firebase not initialized' };
    }

    try {
      const backupRef = doc(this.db, 'backups', backupId);
      const backupSnap = await getDoc(backupRef);

      if (!backupSnap.exists()) {
        return { success: false, error: 'Backup not found' };
      }

      const backupData = backupSnap.data() as ProjectData & { backupId: string };
      const newProjectId = `restored_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

      // Create restored project
      const restoredProject: ProjectData = {
        ...backupData,
        id: newProjectId,
        metadata: {
          ...backupData.metadata,
          createdAt: Timestamp.now(),
          updatedAt: Timestamp.now()
        }
      };

      await setDoc(doc(this.db, 'projects', newProjectId), restoredProject);

      // Add to user's projects
      if (this.currentUser) {
        const userProfile = await this.getUserProfile(this.currentUser.uid);
        if (userProfile) {
          await this.updateUserProfile(this.currentUser.uid, {
            projects: [...userProfile.projects, newProjectId]
          });
        }
      }

      this.emit('projectRestored', { backupId, projectId: newProjectId });
      return { success: true, projectId: newProjectId };
    } catch (error: any) {
      this.emit('restoreError', { backupId, error });
      return { success: false, error: error.message };
    }
  }

  // Advanced storage management
  async listProjectFiles(projectId: string): Promise<Array<{ name: string; url: string; size: number; lastModified: string }>> {
    if (!this.storage) return [];

    try {
      const projectRef = ref(this.storage, `projects/${projectId}`);
      const listResult = await listAll(projectRef);

      const files = await Promise.all(
        listResult.items.map(async (itemRef) => {
          const url = await getDownloadURL(itemRef);
          const metadata = await getMetadata(itemRef);
          return {
            name: itemRef.name,
            url,
            size: metadata.size,
            lastModified: metadata.timeCreated
          };
        })
      );

      return files;
    } catch (error: any) {
      console.error('Failed to list project files:', error);
      return [];
    }
  }

  async getStorageUsage(uid: string): Promise<{ totalUsed: number; breakdown: { [projectId: string]: number } }> {
    if (!this.storage) return { totalUsed: 0, breakdown: {} };

    try {
      const userProfile = await this.getUserProfile(uid);
      if (!userProfile) return { totalUsed: 0, breakdown: {} };

      const breakdown: { [projectId: string]: number } = {};
      let totalUsed = 0;

      for (const projectId of userProfile.projects) {
        const files = await this.listProjectFiles(projectId);
        const projectSize = files.reduce((sum, file) => sum + file.size, 0);
        breakdown[projectId] = projectSize;
        totalUsed += projectSize;
      }

      return { totalUsed, breakdown };
    } catch (error: any) {
      console.error('Failed to get storage usage:', error);
      return { totalUsed: 0, breakdown: {} };
    }
  }

  // Auth state management
  private setupAuthStateListener(): void {
    // This will be called when Firebase is initialized
    setTimeout(() => {
      if (this.auth) {
        onAuthStateChanged(this.auth, (user: any) => {
          this.currentUser = user;
          this.authStateListeners.forEach(listener => listener(user));
        });
      }
    }, 100);
  }

  onAuthStateChanged(callback: (user: User | null) => void): () => void {
    this.authStateListeners.push(callback);
    
    // Return unsubscribe function
    return () => {
      const index = this.authStateListeners.indexOf(callback);
      if (index > -1) {
        this.authStateListeners.splice(index, 1);
      }
    };
  }

  getCurrentUser(): User | null {
    return this.currentUser;
  }

  isAuthenticated(): boolean {
    return this.currentUser !== null;
  }

  // Utility methods
  async testConnection(): Promise<boolean> {
    if (!this.db) return false;

    try {
      // Try to read from a test collection
      const testDoc = doc(this.db, 'test', 'connection');
      await getDoc(testDoc);
      return true;
    } catch (error) {
      console.error('Firebase connection test failed:', error);
      return false;
    }
  }

  disconnect(): void {
    this.app = null;
    this.auth = null;
    this.db = null;
    this.storage = null;
    this.currentUser = null;
    this.authStateListeners = [];
  }
}

// Export singleton instance
export const firebaseService = new FirebaseService();